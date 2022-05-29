# Concall Tools

Collection of scripts to extract information from concall transcripts.

## Installation

```bash
pip install concall-tools
```

## Usage

```python
from concall_tools import extract_speakers

extract_speakers('company-transcript.pdf')
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
