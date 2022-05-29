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
pip install -r requirements/requirements-dev.txt

# run tests
python -m unittest
```
