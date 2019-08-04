# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import binascii

from pybloom_live import BloomFilter


DEFAULT_ERROR = 0.0001
DEFAULT_COLUMN = 1
DEFAULT_COMMENT = "#"


# reference - http://stackoverflow.com/a/9631635
def _blocks(this_file, size=65536):
    while True:
        b = this_file.read(size)
        if not b:
            break
        yield b


def get_number_of_items(infile, skip_first=False, comment_prefix=None):
    with open(infile, "rb") as fh:
        if skip_first:
            # skip first line
            _ = fh.readline()
        num_lines = sum(bl.count(b"\n") for bl in _blocks(fh))
        if comment_prefix:
            num_comment_lines = sum(
                bl.count(b"\n" + comment_prefix.encode("utf-8")) for bl in _blocks(fh)
            )
            num_lines -= num_comment_lines
    return num_lines


def get_items(
    infile, delim=",", column=1, skip_first=False, unhex=False, comment_prefix=None
):
    with open(infile, "r") as fh:
        if skip_first:
            # Strip off header
            _ = fh.readline()
        for line in fh:
            if comment_prefix and line.startswith(comment_prefix):
                continue
            if delim:
                val = line.split(delim)[column - 1].strip('"').rstrip("\r\n")
            else:
                val = line.rstrip("\r\n")
            if val:
                if unhex:
                    val = binascii.unhexlify(val)
                yield val


def build(
    infile,
    outfile,
    error_rate=0.0001,
    delim=None,
    column=1,
    skip_first=False,
    unhex=False,
    comment_prefix=None,
    num_items=None,
):
    print("[BUILDING] Using error-rate: {}".format(error_rate))
    if os.path.isfile(infile):
        print("[BUILDING] Reading in Hashset: {}".format(infile))
        print("[BUILDING] Calculating number of hashes...")
        if not num_items:
            num_items = get_number_of_items(infile, skip_first, comment_prefix)
        print("[BUILDING] There are {} hashes in the Hashset".format(num_items))
        print("[BUILDING] Creating bloomfilter")
        bf = BloomFilter(num_items, error_rate)
        print("[BUILDING] Inserting hashes into bloomfilter")
        for item in get_items(
            infile,
            delim=delim,
            column=column,
            skip_first=skip_first,
            unhex=unhex,
            comment_prefix=comment_prefix,
        ):
            try:
                bf.add(item)
            except Exception as e:
                print("[ERROR] {}".format(e), file=sys.stderr)
        print("[BUILDING] Hashset bloomfilter contains {} items.".format(len(bf)))
        with open(outfile, "wb") as fh:
            bf.tofile(fh)
        print("[BUILDING] Complete")
    else:
        print("[ERROR] No such file or directory: {}".format(infile), file=sys.stderr)

    return


def main(args):
    build(
        args.infile,
        args.outfile,
        args.error,
        args.delim,
        args.column,
        args.skip_first,
        args.hex,
        args.skip_comments,
    )


def _add_subcmd(subparsers):
    builder = subparsers.add_parser("build", help="create a bloomfilter file")
    builder.add_argument("--infile", "-i", required=True, help="Hashset file")
    builder.add_argument("--outfile", "-o", required=True, help="Resulting bloom filter")
    builder.add_argument(
        "--error",
        "-e",
        type=float,
        default=DEFAULT_ERROR,
        help="Error rate (default: {})".format(DEFAULT_ERROR),
    )
    builder.add_argument(
        "--delim", "-d", help="Delimeter (ex: ,), otherwise uses whole line as item"
    )
    builder.add_argument(
        "--column",
        "-c",
        type=int,
        default=DEFAULT_COLUMN,
        help="Column number (default: {}). Requires -d".format(DEFAULT_COLUMN),
    )
    builder.add_argument(
        "--hex",
        action="store_true",
        default=False,
        help="Convert from hexadecimal string to binary before inserting into bloom filter",
    )
    builder.add_argument(
        "--skip-first",
        "--sf",
        dest="skip_first",
        action="store_true",
        default=False,
        help="Skip first line in file",
    )
    builder.add_argument(
        "--skip-comments",
        "--sc",
        dest="skip_comments",
        metavar="COMMENT_PREFIX",
        default=DEFAULT_COMMENT,
        help="Skip lines starting with the given characters (default: {})".format(
            DEFAULT_COMMENT
        ),
    )
    builder.set_defaults(func=main)
