# Concall Tools

Collection of scripts to extract information from concall transcripts.

## Installation

```bash
pip install concall-tools
```

## Usage

```python
from concall_tools import get_speakers

extract_speakers('company-transcript.pdf')
# [
#     Speaker(name="Moderator", firm=None),
#     Speaker(name="Srinivasan V", firm=None),
#     Speaker(name="Mahrukh Adajania", firm="Edelweiss"),
#     Speaker(name="Rahul Jain", firm="Goldman Sachs"),
#     Speaker(name="Aditya Jain", firm="Citigroup"),
#     Speaker(name="Manish Shukla", firm="Axis Capital"),
#     Speaker(name="Sagar Doshi", firm=None),
#     Speaker(name="Adarsh Parasrampuria", firm="CLSA"),
#     Speaker(name="Saurabh", firm="JP Morgan"),
# ]
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
