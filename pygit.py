#!/usr/bin/env python3

import argparse
import configparser
import os

# import sys
# import hashlib
# import configparser
# import zlib


def repo_path(repo, *path):
    """Returns path relative to repo's gitdir root"""
    return os.path.join(repo.gitdir, *path)


def repo_filepath(repo, *path, mkdir=False):
    """Returns path relative to repo's root, creating parent directories if they
    don't exist."""
    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return repo_path(repo, *path)


def repo_dir(repo, *path, mkdir=False):
    """Returns path relative to repo's root, creating parent directories"""
    path = repo_path(repo, *path)

    if os.path.exists(path):
        if os.path.isdir(path):
            return path
        else:
            raise Exception(f"Not a directory {path}")

    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None


def repo_default_config():
    default_config = configparser.ConfigParser()

    default_config.add_section("core")
    default_config.set("core", "repositoryformatversion", "0")
    default_config.set("core", "filemode", "false")
    default_config.set("core", "bare", "false")

    return default_config


def repo_create(path):
    """Creates a new repository at path"""
    repo = Repository(path, True)

    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception(f"{path} is not a directory")
        if os.listdir(repo.worktree):
            raise Exception(f"{path} is not empty")
    else:
        os.makedirs(repo.worktree)

    assert repo_dir(repo, "branches", mkdir=True)
    assert repo_dir(repo, "objects", mkdir=True)
    assert repo_dir(repo, "refs", "tags", mkdir=True)
    assert repo_dir(repo, "refs", "heads", mkdir=True)

    # create .git/description
    with open(repo_filepath(repo, "description"), "w") as f:
        f.write(
            "Unnamed repository; edit this file 'description' to name the repository.\n"
        )

    # create .git/HEAD
    with open(repo_filepath(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    with open(repo_filepath(repo, "config"), "w") as f:
        config = repo_default_config()
        config.write(f)

    return repo


class Repository:
    worktree = None
    gitdir = None
    conf = None

    def __init__(self, path, force_init=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")
        if not (force_init or os.path.isdir(self.gitdir)):
            raise Exception(f"Not a git repository {path}")

        self.conf = configparser.ConfigParser()
        config = repo_filepath(self, "config")

        if config and os.path.exists(config):
            self.conf.read([config])
        elif not force_init:
            raise Exception("Config file missing")

        if not force_init:
            version = int(self.conf.get("core", "repositoryformatversion"))
            if version != 0:
                raise Exception(f"Unsupported repositoryformatversion {version}")


def cmd_add(args):
    return


def cmd_commit(args):
    return


def cmd_init(args):
    repo_create(args.path)
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
    argsp = subparsers.add_parser("init", help="Initialize a new, empty repository")
    argsp.add_argument(
        "path",
        metavar="directory",
        nargs="?",
        default=".",
        help="Where to create the repository",
    )
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
