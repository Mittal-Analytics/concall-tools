import fitz
import enchant


from speakers.extraction import Speaker
from speakers.extraction import (
    get_speakers_from_text as _get_speakers_from_text,
    get_speakers_in_bold as _get_speakers_in_bold,
    get_speakers_capitals as _get_speakers_capitals
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
    if algorithm not in ["bold", "plain", "auto",]:
        raise ValueError("algorithm must be one of 'bold', 'plain', 'auto'")

    doc = fitz.open(pdf_name)
    speakers = []
    names_from_plain_bold=[]
    speakers_common=[]
    if algorithm == "auto" or algorithm == "bold":
        speakers = _get_speakers_in_bold(doc)
    if not speakers and (algorithm == "auto" or algorithm == "plain"):
        speakers = _get_speakers_from_text(doc)
    speakers_in_capital=_get_speakers_capitals(pdf_name)
    for name,firm in speakers:
        names_from_plain_bold.append(name)
    for speaker in speakers_in_capital:
        if speaker.name in names_from_plain_bold:
            speakers_common.append(speaker)
        if speaker.name not in names_from_plain_bold:
            if speaker.firm!=None:
                speakers_common.append(speaker)
    return speakers_common