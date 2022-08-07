#!/usr/bin/env python3

import argparse
import os
import sys
import hashlib
import configparser
import zlib


def cmd_add(args):
    return


def cmd_commit(args):
    return


def cmd_init(args):
    return


def cmd_log(args):
    return


def cmd_switch(args):
    return


def cmd_restore(args):
    return


def main():
    parser = argparse.ArgumentParser(
        description="Implementation of a simple git client in Python"
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    subparsers.required = True
    args = parser.parse_args()

    if args.command == "add":
        cmd_add(args)
    elif args.command == "commit":
        cmd_commit(args)
    elif args.command == "init":
        cmd_init(args)
    elif args.command == "log":
        cmd_log(args)
    elif args.command == "switch":
        cmd_switch(args)
    elif args.command == "restore":
        cmd_restore(args)


if __name__ == "__main__":
    main()
