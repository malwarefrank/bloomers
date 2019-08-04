Bloomers
========

Easily create file-backed bloom filters from lots of data.  My primary purpose is for hashsets, but it should be general enough to use for any other strings.

The code is _heavily_ based on https://github.com/blacktop/docker-nsrl

Quick start
-----------

- Treat each line in ```INFILE``` as a single item, create a bloom filter (with default error rate), add the items to the bloom filter, and persist it to OUTFILE

```bash
$ pip3 install .
$ bloomers build -i INFILE -o OUTFILE
```

- Do the same thing, but for comma-delimited input (will auto-remove double-quotes), only take the second column from each row, and assume it is a hexadecimal string

```bash
$ bloomers build -i INFILE -o OUTFILE -d , -c 2 --hex
```

- Check if any of a set of hashes exist in the bloom filter

```bash
$ bloomers search -i INFILE --csv --hex HASH1 HASH2 HASH3 HASH4
```
