import re
from collections import namedtuple

import nltk

from .pdf_utils import get_text
from .stop_words import STOP_WORDS

Speaker = namedtuple("Speaker", ["name", "firm"])


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
    return " ".join(word.rsplit("/", 1)[0] for word in subjtext.split(" "))


def _extract_relations(named_tags):
    """
    Extract name fo firm from which the speaker is associated
    """
    # extract speaker names and firms
    speaker_firm = {}
    FROM = re.compile(r".*\bfrom\b.*")
    relations = nltk.sem.extract_rels(
        "PERSON", "ORGANIZATION", named_tags, pattern=FROM
    )
    for relation in relations:
        speaker = _get_fingerprint(_extract_name(relation["subjtext"]))
        firm = _extract_name(relation["objtext"])
        if speaker not in speaker_firm:
            speaker_firm[speaker] = firm
    # sometimes the relationship is in form of PERSON PERSON
    relations = nltk.sem.extract_rels(
        "PERSON", "PERSON", named_tags, pattern=FROM
    )
    for relation in relations:
        speaker = _get_fingerprint(_extract_name(relation["subjtext"]))
        firm = _extract_name(relation["objtext"])
        if speaker not in speaker_firm:
            speaker_firm[speaker] = firm
    print(speaker_firm)
    return speaker_firm


def extract_speakers(pdf_name):
    pages = get_text(pdf_name)
    text = ""
    for i, page in enumerate(pages):
        # a transcript page would have at-least 100 words
        word_count = len(page.split())
        if word_count < 150 or i == len(pages) - 1:
            continue
        text += "\n\n" + page

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
    for person in people:
        is_speaker = any(line.startswith(person) for line in text.split("\n"))
        if is_speaker:
            fp = _get_fingerprint(person)
            speaker = Speaker(name=person, firm=speaker_firm.get(fp, None))
            speakers.append(speaker)
    return speakers
