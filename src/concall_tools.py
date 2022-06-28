import fitz
import enchant
d = enchant.Dict("en_US")

from speakers.extraction import Speaker
from speakers.extraction import (
    get_speakers_from_text as _get_speakers_from_text,
)
from speakers.extraction import get_speakers_in_bold as _get_speakers_in_bold
from speakers.extraction import get_speakers_capitals as _get_speakers_capitals


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
    if algorithm not in ["bold", "plain", "auto"]:
        raise ValueError("algorithm must be one of 'bold', 'plain', 'auto'")

    doc = fitz.open(pdf_name)
    speakers = []
    names=[]
    speakers2=[]
    if algorithm == "auto" or algorithm == "bold":
        speakers = _get_speakers_in_bold(doc)
    if not speakers and (algorithm == "auto" or algorithm == "plain"):
        speakers = _get_speakers_from_text(doc)
    speakers1=_get_speakers_capitals(pdf_name)
    for s in speakers:
        names.append(s[0])
    #print(names)
    for s in speakers1:
        if s[0] in names:
            speakers2.append(s)
        if s[0] not in names:
            if s[1]!=None:
                speakers2.append(s)
    #print(speakers2)
    return speakers2