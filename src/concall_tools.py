import fitz

from speakers.extraction import Speaker
from speakers.extraction import (
    get_speakers_from_text as _get_speakers_from_text,
)
from speakers.extraction import get_speakers_in_bold as _get_speakers_in_bold


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
    if algorithm == "auto" or algorithm == "bold":
        speakers = _get_speakers_in_bold(doc)
    if not speakers and (algorithm == "auto" or algorithm == "plain"):
        speakers = _get_speakers_from_text(doc)
    return speakers
