import sys
import argparse

from .build import _add_subcmd as _add_build_cmd
from .search import _add_subcmd as _add_search_cmd


def cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    _add_build_cmd(subparsers)
    _add_search_cmd(subparsers)

    args = parser.parse_args()
    args.func(args)
