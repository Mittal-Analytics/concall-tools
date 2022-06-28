import re
from collections import namedtuple

import lxml.html
import nltk
import fitz
import enchant
dictionary = enchant.Dict("en_US")

Speaker = namedtuple("Speaker", ["name", "firm"])


def _get_pages(doc):
    Page = namedtuple("Page", ["page", "number", "text", "word_count"])
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        page = Page(
            page=page,
            number=i,
            text=text,
            word_count=len(text.split()),
        )
        pages.append(page)
    return pages


def _get_main_pages(doc):
    pages = _get_pages(doc)

    # get median word count
    word_counts = [page.word_count for page in pages]
    median = sorted(word_counts)[len(word_counts) // 2]
    # main pages are pages with at-least half as much text
    main_pages = [page for page in pages if page.word_count > (median / 4) and page.number!=0]
    return main_pages


def _get_fingerprint(name):
    """
    returns a generic name without prefixes
    it helps match: "Mr. Praveen Arora" and "Praveen Arora"
    it does by return a normalized version: praveenarora
    """
    original_name = name.replace("\n", " ").strip()
    NON_WORD = re.compile(r"[\W]+")
    name = NON_WORD.sub(" ", original_name).lower()

    removals = [
        r"^the ",
        r" and ",
        r"^mr ",
        r"^mrs ",
        r"^ms ",
    ]
    for removal in removals:
        name = re.sub(removal, "", name)

    # join everything
    name = name.replace(" ", "")
    return name


def _extract_name(subjtext):
    """
    the extract_rels function returns a string with the POS tags in it
    this function extracts the name from the string
    """
    return " ".join(
        nltk.tag.str2tuple(word)[0] for word in subjtext.split(" ")
    )


def _get_relations(named_tags, subjclass, objclass):
    """
    Extract relations between two named entities
    """
    FROM = re.compile(r".*\bfrom\b.*")
    relations = nltk.sem.extract_rels(
        subjclass, objclass, named_tags, pattern=FROM
    )
    speaker_firm = {}
    for relation in relations:
        speaker = _get_fingerprint(_extract_name(relation["subjtext"]))
        firm = _extract_name(relation["objtext"])
        if speaker not in speaker_firm:
            speaker_firm[speaker] = firm
    return speaker_firm


def _tree2str(tree):
    return " ".join(w for w, _t in tree.leaves())


def _manual_chunk(named_tags):
    pos_tags = [
        (w, t) for w, t, _iob in nltk.chunk.util.tree2conlltags(named_tags)
    ]
    pos_tags = [
        ("from", "FROM") if w == "from" else (w, t) for w, t in pos_tags
    ]

    grammar = r"""
        FIR: {<JJ>? <NNP.*>+ <IN|CC> <NNP.*> <NN.*>*}
        PER: {<JJ>? <NNP.*>+ <NN.*>*}
        REL: {<PER> <,>? <FROM> <FIR> <.|,>}
             {<PER> <,>? <FROM> <PER>}
             {<PER> <\(> <PER> <\)>}
             {<PER> <,> <PER>}
    """
    cp = nltk.RegexpParser(grammar)
    tree = cp.parse(pos_tags)
    speaker__firm = {}
    for subtree in tree.subtrees():
        if subtree.label() == "REL":
            entities = [
                _tree2str(t)
                for t in subtree.subtrees()
                if t.label() in ["PER", "FIR"]
            ]
            speaker, firm = entities
            key = _get_fingerprint(speaker)
            if key not in speaker__firm:
                speaker__firm[key] = firm
    return speaker__firm


def _extract_relations(named_tags):
    """
    Extract name fo firm from which the speaker is associated
    """
    # extract all relations in form of: NOUN from NOUN
    speaker_firm = _manual_chunk(named_tags)

    # try named-entity relations if no manual relation found
    for speaker, firm in _get_relations(
        named_tags, "PERSON", "ORGANIZATION"
    ).items():
        if speaker not in speaker_firm:
            speaker_firm[speaker] = firm

    # sometimes, the named entity tags ORGANIZATION as PERSON
    # thus try PERSON from PERSON if not available
    for speaker, firm in _get_relations(
        named_tags, "PERSON", "PERSON"
    ).items():
        if speaker not in speaker_firm:
            speaker_firm[speaker] = firm
    return speaker_firm


def _print_portion(named_tags, substr):
    conll_tags = nltk.chunk.util.tree2conlltags(named_tags)
    all_tokens = [w for w, _t, _iob in conll_tags]
    look_tokens = nltk.word_tokenize(substr)

    for i in range(len(all_tokens) - len(look_tokens) + 1):
        portion = all_tokens[i : i + len(look_tokens)]
        if portion == look_tokens:
            print("PORTION:", conll_tags[i : i + len(look_tokens)])
            return


def _assert_same(lines, sent_lines, row_pos, col_pos):
    for sent_line in sent_lines[:-1]:
        assert lines[row_pos] == sent_line
        row_pos += 1
        col_pos = 0
    if sent_lines:
        last_sent_line = sent_lines[-1]
        compared_line = lines[row_pos]
        assert compared_line.startswith(last_sent_line)
        row_pos += 1
        col_pos = len(last_sent_line)
    return row_pos, col_pos


def _get_text_blocks(text):
    """
    Returns text blocks (paragraphs)

    Algorithm:
    - tokenize text into sentences
    - also split text into lines
    - it is a paragraph if the sentence is also a new line
    """
    text = text.replace("Pvt.", "Pvt")
    sentences = nltk.sent_tokenize(text)
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    row_pos = 0
    col_pos = 0
    paragraphs = []
    buffer = []
    while sentences:
        sentence = sentences.pop(0)
        sent_lines = [l.strip() for l in sentence.splitlines() if l.strip()]
        assert lines[row_pos][col_pos:].strip().startswith(sent_lines[0])
        col_pos = lines[row_pos].index(sent_lines[0], col_pos) + len(
            sent_lines[0]
        )
        row_pos, col_pos = _assert_same(
            lines[1:], sent_lines[1:], row_pos, col_pos
        )
        buffer.append(sentence)
        if col_pos == len(lines[row_pos]):
            paragraphs.append(" ".join(buffer))
            buffer = []
            row_pos += 1
            col_pos = 0
    return paragraphs


def _cleanup_people(text, people):
    is_all_caps = all(w.isupper() for w in people)
    if not is_all_caps:
        people = [person for person in people if not person.isupper()]

    # any valid person will be there at-least twice in concall
    people = [person for person in people if text.count(person) > 1]
    return people


def get_speakers_from_text(doc):
    pages = _get_main_pages(doc)
    text = "\n".join([page.text for page in pages])

    # extract people
    paragraphs = _get_text_blocks(text)
    people = []
    for paragraph in paragraphs:
        pos_tag = nltk.pos_tag(nltk.word_tokenize(paragraph))

        # a person name is either before a ":"
        # or is the full line itself
        lines = paragraph.splitlines()
        person = lines[0]
        if ":" in person:
            person = person.split(":", 1)[0]
        person = person.strip()

        # tokenize first_line using pos_tag
        words = nltk.word_tokenize(person)
        tagged_words = pos_tag[: len(words)]

        is_name = (
            _is_name(person)
            and all(
                t in ["NN", "NNS", "NNP", "NNPS", ".", "JJ"]
                for w, t in tagged_words
            )
            and "NNP" in [t for w, t in tagged_words]
            # exclude tables and broken text blocks
            # a conversation would have at-least 4 words per line
            and len(pos_tag) / len(lines) > 4
        )
        if is_name and person not in people:
            people.append(person)
    people = _cleanup_people(text, people)

    # tokenize the text and recognize named entities
    named_tags = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(text)))
    speaker_firm = _extract_relations(named_tags)

    speakers = []
    for person in people:
        fp = _get_fingerprint(person)
        speaker = Speaker(name=person, firm=speaker_firm.get(fp, None))
        speakers.append(speaker)
    return speakers


def _get_plain_text_word_count(el):
    word_count = 0
    if el is not None and el.tag != "b":
        if el.text:
            word_count += len(el.text.split())
        for child in el.getchildren():
            word_count += _get_plain_text_word_count(child)
    return word_count


def _is_text_block_child(el):
    """
    returns true if the element has a following paragraph
    """
    parent = el.getparent()
    word_count = _get_plain_text_word_count(parent)

    next_block = parent.getnext()
    if next_block is not None and not next_block.text_content().strip():
        next_block = next_block.getnext()
    word_count = _get_plain_text_word_count(next_block)
    return word_count >= 5


def _is_name(text):
    if "," in text:
        return False
    # remove all non-alphanumeric characters
    text = re.sub(r"[^a-zA-Z\s]", "", text).strip()
    return len(text) > 2 and len(text.split()) <= 5


def get_speakers_in_bold(doc):
    people = []
    pages = _get_main_pages(doc)
    for page in pages:
        html = page.page.get_text("html")
        tree = lxml.html.fromstring(html)
        bolds = tree.cssselect("b")
        for bold in bolds:
            is_first_child = bold.getprevious() is None
            if not is_first_child:
                continue
            text = bold.text_content().strip().strip(":").strip()
            is_person = text and _is_text_block_child(bold) and _is_name(text)
            if is_person:
                people.append(text)

    text = "\n".join([page.text for page in pages])
    people = _cleanup_people(text, people)

    # get relations
    text = "\n".join(page.text for page in pages)
    named_tags = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(text)))
    speaker_firm = _extract_relations(named_tags)

    speakers = []
    for person in people:
        fp = _get_fingerprint(person)
        speaker = Speaker(name=person, firm=speaker_firm.get(fp, None))
        if speaker not in speakers:
            speakers.append(speaker)
    return speakers


def get_lines(doc):
    doc=fitz.open(doc)
    pages=_get_main_pages(doc)
    text = "\n".join([page.text for page in pages])
    text = text.replace("Pvt.", "Pvt")
    text = text.replace(":",":\n")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return lines


def check_last_char(names):
    count=0
    names_temp=[]
    for name in names:
        if name[-1]==':':
            count=count+1
    names_temp=names
    names=[]
    for name in names_temp:
        if count/len(names_temp)>0.40:
            if name[-1]==':':
                names.append(name)
        elif name[-1]!=':' and name[-1]!='.':
            names.append(name)
    return names


def remove_last_char_if_colon(word):
    if word[-1]==':':
        word=word[0:len(word)-1]
    return word


def check_dict(names):
    names_temp=names
    names=[]
    possible_names_in_dictionary=['Shah','Moderator','moderator','Raj','Participant']
    for name in names_temp:
        count=0
        for word in name.split():
            word=remove_last_char_if_colon(word)
            if dictionary.check(word) and word not in possible_names_in_dictionary:
                count=count+1
            if name=='KFin':
                count=count+1
        if count/len(name.split())<=0.50:
            names.append(name)
    return names


def check_repetations(names):
    names_temp=names
    for name_outer in names:
        for name_inner in names:
            if name_outer.find(name_inner)!=-1 and len(name_outer)>len(name_inner):
                names_temp.remove(name_inner)
    names=names_temp
    return(names)


def get_speaker_names(doc):
    lines = get_lines(doc)
    char_not_in_names=[',','-','&','?']
    names=[]
    converse=[]
    for line in lines:
        flag=0
        words=line.split()
        if len(words)<=5 or (words[0]=="Moderator" or words[0]=='Moderator:'): 
            if len(words)==1 and len(words[0])<4:
                flag=1
            for word in words:
                if not word[0].isupper():
                    flag=1
                for letter in word:
                    if letter.isnumeric() or letter in char_not_in_names:
                        flag=1
            if flag==0:
                if line not in names:
                    names.append(line)
    names=check_dict(names)
    names=check_last_char(names)
    names=check_repetations(names)
    for line in lines:
        if line in names:
            converse.append(line)
    return [names,lines,converse]


def get_conversation(doc):
    names,lines,converse=get_speaker_names(doc)
    s=''
    conversation=[]
    for line in lines:
        if line not in names:
            s=s+line+' '
        else:
            conversation.append(s)
            s=''
    if s!='':
        conversation.append(s)
    conversation_from_beginning=conversation
    conversation=conversation[1:len(conversation)]
    return (conversation,conversation_from_beginning)


def modify_str(l):
    str=l.replace('.','. ')
    l=l.replace(',',', ')
    l=l.replace('from','from ')
    l=l.replace('(','')
    l=l.replace(')','.')
    w=l.split()
    return w


def find_count(name,w,count_max):
    flag=0
    position=0
    count=0
    name_index=0
    for word in name.split():
        word=remove_last_char_if_colon(word)
        if word in w:
            if flag==0:
                name_index=w.index(word)
                flag=1
            count=count+1
        elif flag==0:
            position=position+1
    if count>count_max:
        count_max=count
    return (count,count_max,position,name_index)


def pass_1(names,conversation,converse):
    final={}
    for name in names:
        name=remove_last_char_if_colon(name)
        count_max=0
        for i in range(len(conversation)):
            if converse[i]=='Moderator:' or converse[i]=='Moderator' or converse[i]=='Operator' or converse[i]=='Operator:':
                count=0
                l=conversation[i]
                #modify_str takes the conversation, makes some changes and returns the words to w
                w=modify_str(l)
                #postion is the postion of the word identified in name 
                #name_index is the postion of the word identified in w                
                count,count_max,position,name_index=find_count(name,w,count_max)
                if count/len(name.split())>=0.5 and count>=count_max:
                    flag_2=0
                    flag_3=0
                    firm=''
                    for c in range(name_index+len(name.split())-position,len(w)):
                        if ((w[c][0].isupper() or w[c]=='individual') and flag_2==0 and w[c]!='Sir,'):
                            flag_2=1
                            b=((w[c][-1]=='.' or w[c][-1]==','))
                            while not b:
                                firm=firm+w[c]+' '
                                c=c+1
                                if c==len(w):
                                    for letter in firm:
                                        if letter.isnumeric():
                                            firm=''
                                    flag_3=1
                                    break
                                b=((w[c][-1]=='.' or w[c][-1]==','))
                            if flag_3==0:
                                firm=firm+w[c]
                    firm=firm[0:len(firm)-1]
                    if len(firm.split())>5:
                        firm=''
                    if name[-1]==':':
                        name=name[0:len(name)-1]
                    final[name]=firm
    return final


def pass_2(names,conversation,converse,final):
    for name in names:
        count_max=0
        name=remove_last_char_if_colon(name)
        if name not in final.keys() or final[name]=='':
            for i in range(len(conversation)):
                converse[i]=remove_last_char_if_colon(converse[i])
                if converse[i]==name:
                    count=0
                    l=conversation[i]
                    l=conversation[i]
                    #modify_str takes the conversation, makes some changes and returns the words to w
                    w=modify_str(l)
                    #postion is the postion of the word identified in name 
                    #name_index is the postion of the word identified in w
                    count,count_max,position,name_index=find_count(name,w,count_max)
                    if count/len(name.split())>=0.33 and count>=count_max:
                        flag_2=0
                        flag_3=0
                        firm=''
                        for c in range(name_index+len(name.split())-position,len(w)):
                            if ((w[c][0].isupper() or w[c]=='individual') and flag_2==0 and w[c]!='Sir,' and w[c]!='I'):
                                flag_2=1
                                b=((w[c][-1]=='.' or w[c][-1]==','))
                                while not b:
                                    firm=firm+w[c]+' '
                                    c=c+1
                                    if c==len(w):
                                        for letter in firm:
                                            if letter.isnumeric():
                                                firm=''
                                        flag_3=1
                                        break
                                    b=((w[c][-1]=='.' or w[c][-1]==','))
                                if flag_3==0:
                                    firm=firm+w[c]
                        firm=firm[0:len(firm)-1]
                        if len(firm.split())>5:
                            firm=''
                        if name[-1]==':':
                            name=name[0:len(name)-1]
                        final[name]=firm
    return final


def pass_3(names,conversation_from_beginning,converse,final):
    for name in names:
        count_max=0
        name=remove_last_char_if_colon(name)
        if name not in final.keys() or final[name]=='':
            for i in range(3):
                if name not in final.keys() or final[name]=='':
                    count=0
                    l=conversation_from_beginning[i]
                    #modify_str takes the conversation, makes some changes and returns the words to w
                    w=modify_str(l)
                    #postion is the postion of the word identified in name 
                    #name_index is the postion of the word identified in w
                    count,count_max,position,name_index=find_count(name,w,count_max)
                    if count/len(name.split())>=0.5 and count>=count_max:
                        flag_2=0
                        flag_3=0
                        firm=''
                        for c in range(name_index+len(name.split())-position,len(w)):
                            if ((w[c][0].isupper() or w[c]=='individual') and flag_2==0 and w[c]!='Sir,'):
                                flag_2=1
                                b=((w[c][-1]=='.' or w[c][-1]==','))
                                while not b:
                                    firm=firm+w[c]+' '
                                    c=c+1
                                    if c==len(w):
                                        for letter in firm:
                                            if letter.isnumeric():
                                                firm=''
                                        flag_3=1
                                        break
                                    b=((w[c][-1]=='.' or w[c][-1]==',' or w[c][-1]==';' or w[c]=='and' or w[c]=='May'))
                                if flag_3==0 and w[c]!='and' and w[c]!='May':
                                    firm=firm+w[c]
                        firm=firm[0:len(firm)-1]
                        if len(firm.split())>5:
                            firm=''
                        for letter in firm:
                            if letter.isnumeric():
                                firm=''
                        if name[-1]==':':
                            name=name[0:len(name)-1]
                        final[name]=firm
    return final


def get_speakers_capitals(doc):    
    names,lines,converse=get_speaker_names(doc)
    conversation,conversation_from_beginning=get_conversation(doc)
    final={}
    #pass 1 checks if the moderator announces any names
    final=pass_1(names,conversation,converse)
    #pass 2 checks if incase moderator has not introduced, if the speaker introduces himself
    final=pass_2(names,conversation,converse,final)
    #for speakers whose firm is still unknown, we check the first 3 conversations to check if they are introduced as management
    final=pass_3(names,conversation_from_beginning,converse,final)
    for name in names:
        name=remove_last_char_if_colon(name)
        if name not in final.keys() or final[name]=='':
            final[name]=None
    speakers=[]
    names_temp=[]
    #names_temp is created so that the order in which speakers speak is mantained in the final tuple
    for name in names:
        name=remove_last_char_if_colon(name)
        names_temp.append(name)
    for name in names_temp:
        speaker = Speaker(name=name, firm=final[name])
        speakers.append(speaker)
    return speakers



