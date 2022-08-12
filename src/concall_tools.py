import fitz
import enchant


from speakers.extraction import (
    Speaker,
    Speaker_with_is_management
)
from speakers.extraction import (
    get_speakers_from_text as _get_speakers_from_text,
    get_speakers_in_bold as _get_speakers_in_bold,
    get_speakers_capitals as _get_speakers_capitals,
    get_lines as _get_lines,
    remove_last_char_if_colon as _remove_last_char_if_colon
)



def get_speakers(pdf_name, algorithm="auto"):
    """
    returns list of speakers in the given pdf name

    we have two algorithms for fetching speakers:
    - extract from bold text
    - extract from plain text

    supported values for algorithm:
    - bold
    - plain
    - auto
    """
    if algorithm not in ["bold", "plain", "auto", "Capitals"]:
        raise ValueError("algorithm must be one of 'bold', 'plain', 'auto' ")
    doc = fitz.open(pdf_name)
    speakers = []
    speakers_common = []
    names_from_plain_bold = []
    if algorithm == "auto" or algorithm == "bold":
        speakers = _get_speakers_in_bold(doc)
    if not speakers and (algorithm == "auto" or algorithm == "plain"):
        speakers = _get_speakers_from_text(doc)
    if algorithm in ["bold",'plain']:
        return speakers
    else:
        speakers_in_capital = _get_speakers_capitals(pdf_name)
        for name,firm in speakers:
            names_from_plain_bold.append(name)
        for speaker in speakers_in_capital:
            if speaker.name in names_from_plain_bold:
                speakers_common.append(speaker)
            else:
                if speaker.firm!=None:
                    speakers_common.append(speaker)
        return speakers_common

def get_conversations(pdf_name):
    speakers_common=get_speakers(pdf_name)
    names=[]
    conversation=[]
    conversation_with_speaker=[]
    order_of_speakers=[]
    lines=[]
    s=''
    lines=_get_lines(pdf_name)
    for speaker in speakers_common:
        names.append(speaker[0])
    flag=0
    for line in lines:
        line=_remove_last_char_if_colon(line)
        if line in names:
            order_of_speakers.append(line)
        if line not in names:
            s = s + line + ' '
        else:
            if flag == 1:
                conversation.append(s)
            flag=1
            s=''
    if s!='':
        conversation.append(s)
    for i in range(len(order_of_speakers)):
        for speaker in speakers_common:
            if speaker[0]==order_of_speakers[i]:
                conversation_with_speaker.append((speaker,conversation[i]))
    return conversation_with_speaker
    