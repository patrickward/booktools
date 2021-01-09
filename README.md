# booktools

Repository of scripts for obtaining book data

## isbn.py

Takes a csv as input with "Title" and "Author" columns, and outputs a json of book data with ISBN, ISBN-13, Descriptions, Cover Images, etc.

Usage:

```bash
./isbn.py <in-file>.csv <out-file>.json
```

You can also convert the generated json to a csv file:

```bash
./isbn.py csv <in-file>.json <out-file>.csv
```

