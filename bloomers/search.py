#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import binascii

from pybloom_live import BloomFilter


def _open_bloom(infile):
    nb = open(infile, "rb")
    return BloomFilter.fromfile(nb)


def items_exist(infile, items, unhex=False):
    bf = _open_bloom(infile)
    for v in items:
        if unhex:
            result = binascii.unhexlify(v) in bf
        else:
            result = v in bf
        yield v, result


def main(args):
    for v, result in items_exist(args.infile, args.values, unhex=args.hex):
        if args.csv:
            print("{},{}".format(v, result))
        elif args.verbose:
            if result:
                print("Value {} found in Database.".format(v))
            else:
                print("Value {} was NOT found in Database.".format(v))
        else:
            print(result)
    return


def _add_subcmd(subparsers):
    searcher = subparsers.add_parser("search", help="check if items were added to bloomfilter file")
    searcher.add_argument(
        "--infile", "-i", required=True, help="Bloom filter database to search"
    )
    searcher.add_argument(
        "--verbose",
        "-v",
        help="Display verbose output message",
        action="store_true",
        default=False,
    )
    searcher.add_argument(
        "--csv", action="store_true", default=False, help="Output in csv format"
    )
    searcher.add_argument(
        "--hex",
        action="store_true",
        default=False,
        help="Convert from hex string to binary before searching",
    )
    searcher.add_argument(
        "values", metavar="VALUE", type=str, nargs="+", help="A value to search for"
    )
    searcher.set_defaults(func=main)
