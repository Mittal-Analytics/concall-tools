# Concall Tools

Collection of scripts to extract information from concall transcripts.

## Installation

```bash
pip install concall-tools
```

## Usage

These are the main functions.

**Get Speakers**

Returns an array of speakers in the transcript.

```python
from concall_tools import get_speakers

extract_speakers('company-transcript.pdf')
# [
#     Speaker(name="Moderator", firm=None, is_management=False),
#     Speaker(name="Srinivasan V", firm=None, is_management=True),
#     Speaker(name="Mahrukh Adajania", firm="Edelweiss", is_management=False),
#     Speaker(name="Rahul Jain", firm="Goldman Sachs", is_management=False),
#     Speaker(name="Aditya Jain", firm="Citigroup", is_management=False),
#     Speaker(name="Manish Shukla", firm="Axis Capital", is_management=False),
#     Speaker(name="Sagar Doshi", firm=None, is_management=False),
#     Speaker(name="Adarsh Parasrampuria", firm="CLSA", is_management=False),
#     Speaker(name="Saurabh", firm="JP Morgan", is_management=False),
# ]
```

**Get Conversations**

Returns an array of conversations. Each conversations is a tuple of `(speaker, text)`.

```python
from concall_tools import get_conversations

get_conversations('company-transcript.pdf')
# [
#       (
#           Speaker(name="Moderator", firm=None),
#           "Hi everyone, I am Moderator. I am here to help you with the questions you may have."
#       ),
#       (
#           Speaker(name="Srinivasan V", firm=None),
#           "Hi everyone, I am Srinivasan V. I am here to help you with the questions you may have."
#       ),
#       ...
# ]
```

**Get Summary**

Returns a summary of the transcript. The summary is of all the conversations by the management.

```python
from concall_tools import get_summary

get_summary('company-transcript.pdf')
# """
# We expect a growth of 25%.
# The capex of the company is expected to be around 200 cr.
# To be completed by Q2.
# ...
# """
```


## Development

```bash
python3 -m venv .venv
python -m pip install -e .

# run tests
python -m unittest
```

For publishing:

```bash
bumpver update --minor
python -m build
twine upload dist/*
```
