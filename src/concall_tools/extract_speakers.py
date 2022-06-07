import re
from collections import namedtuple

import fitz
import lxml.html
import nltk

from .stop_words import STOP_WORDS

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
    main_pages = [page for page in pages if page.word_count > (median / 2)]
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


def _manual_chunk(named_tags):
    pos_tags = [
        (w, t) for w, t, _iob in nltk.chunk.util.tree2conlltags(named_tags)
    ]
    pos_tags = [
        ("from", "FROM") if w_t == ("from", "IN") else w_t for w_t in pos_tags
    ]

    grammar = "REL: {<NN.*>+ <FROM> <NN.*>+}"
    cp = nltk.RegexpParser(grammar)
    tree = cp.parse(pos_tags)
    speaker__firm = {}
    for subtree in tree.subtrees():
        if subtree.label() == "REL":
            split_pos = subtree.leaves().index(("from", "FROM"))
            speaker = " ".join(w for w, t in subtree.leaves()[:split_pos])
            firm = " ".join(w for w, t in subtree.leaves()[split_pos + 1 :])
            speaker__firm[_get_fingerprint(speaker)] = firm
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


def _extract_speakers_two(doc):
    pages = [page.get_text("text") for page in doc]
    text = "\n".join(
        page
        for i, page in enumerate(pages)
        # a transcript page would have at-least 150 words
        # or is last page
        if len(page.split()) > 150 or i == len(pages) - 1
    )

    # tokenize the text and recognize named entities
    named_tags = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(text)))

    speaker_firm = _extract_relations(named_tags)

    # extract all speakers
    # by looping over all named entities
    # an entity is a speaker
    # if their name is the first word of any line
    people = []
    for entity in named_tags:
        if isinstance(entity, nltk.tree.Tree) and entity.label() == "PERSON":
            person = " ".join(leaf[0] for leaf in entity.leaves())
            if person.lower() in STOP_WORDS:
                continue
            if person not in people:
                people.append(person)

    speakers = []
    lines = nltk.tokenize.sent_tokenize(text)
    for person in people:
        speaker_lines = [line for line in lines if line.startswith(person)]
        if speaker_lines:
            print("PERSON:", person)
            _print_portion(named_tags, speaker_lines[0])
            fp = _get_fingerprint(person)
            speaker = Speaker(name=person, firm=speaker_firm.get(fp, None))
            speakers.append(speaker)
    return speakers


def _is_text_block_child(el):
    """
    returns true if the element has a following paragraph
    """
    parent = el.getparent()
    next_parent = parent.getnext()
    word_count = len(
        next_parent.text_content().split() + parent.text_content().split()
    )
    return word_count >= 8


def _is_name(text):
    # remove all non-alphanumeric characters
    text = re.sub(r"[^a-zA-Z\s]", "", text).strip()
    return len(text) > 2 and len(text.split()) <= 5


def _extract_speakers_in_bold(doc):
    people = []
    pages = _get_main_pages(doc)
    for page in pages:
        html = page.page.get_text("html")
        tree = lxml.html.fromstring(html)
        bolds = tree.cssselect("b")
        for bold in bolds:
            text = bold.text_content().strip().strip(":").strip()
            is_person = text and _is_text_block_child(bold) and _is_name(text)
            if is_person:
                people.append(text)

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


def extract_speakers(pdf_name):
    doc = fitz.open(pdf_name)
    speakers = _extract_speakers_in_bold(doc)
    return speakers
