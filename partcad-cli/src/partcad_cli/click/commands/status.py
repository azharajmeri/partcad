# OpenVMP, 2023
#
# Author: Roman Kuzmenko, Aleksandr Ilin
# Created: 2024-02-18
#
# Licensed under Apache License, Version 2.0.
#


import rich_click as click

import os
import threading

from partcad import __version__ as version
import partcad.logging as logging

def get_size(start_path="."):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def get_total(path):
    with logging.Action("Status", "total"):
        total = (get_size(path)) / 1048576.0
        logging.info("Total internal data storage size: %.2fMB" % total)


def get_git(path):
    with logging.Action("Status", "git"):
        git_path = os.path.join(path, "git")
        git_total = (get_size(git_path)) / 1048576.0
        logging.info("Git cache size: %.2fMB" % git_total)


def get_tar(path):
    with logging.Action("Status", "tar"):
        tar_path = os.path.join(path, "tar")
        tar_total = (get_size(tar_path)) / 1048576.0
        logging.info("Tar cache size: %.2fMB" % tar_total)


def get_sandbox(path):
    with logging.Action("Status", "sandbox"):
        sandbox_path = os.path.join(path, "sandbox")
        sandbox_total = (get_size(sandbox_path)) / 1048576.0
        logging.info("Sandbox environments size: %.2fMB" % sandbox_total)


@click.command(help="Display the state of internal data used by PartCAD")
@click.pass_obj
def cli(ctx) -> None:
    path = ctx.user_config.internal_state_dir
    with logging.Process("Status", "this"):

        logging.info(f"PartCAD version: {version}")

        # TODO-108: @alexanderilyin: show detail about loaded partcad.yaml
        logging.info("Internal data storage location: %s" % path)

        # Create threads
        thread_total = threading.Thread(target=get_total, args=(path,))
        thread_git = threading.Thread(target=get_git, args=(path,))
        thread_tar = threading.Thread(target=get_tar, args=(path,))
        thread_sandbox = threading.Thread(target=get_sandbox, args=(path,))

        # Launch threads
        thread_total.start()
        thread_git.start()
        thread_tar.start()
        thread_sandbox.start()

        # Wait for threads to finish
        thread_total.join()
        thread_git.join()
        thread_tar.join()
        thread_sandbox.join()
