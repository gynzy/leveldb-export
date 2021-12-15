# LevelDB Export

This package allows to export documents from a LevelDB file. For instance it can be used to extract documents from a previously created Firestore export. Note, this package is a fork from [labbots/firestore-export-json](https://github.com/labbots/firestore-export-json). This fork is different in:

1. Makes it an installable package. The original is designed to run as a script.
2. Solves some parsing issues regarding arrays.


## Installation

Install the package from pypi.

```bash
pip install leveldb-export
```

## Example

Use the function `parse_leveldb_documents` to parse documents from a LevelDB / Firestore dump. As input either:

- Use path to file
- Use open file handle

For example

```python
>>> from leveldb_export import parse_leveldb_documents
>>> docs = list(parse_leveldb_documents("./firestore/export-0"))
>>> print(f"Got {len(docs)} documents")
Got 288 documents
```
