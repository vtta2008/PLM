# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------

import os, contextlib, click, requests_cache

from PLM.api.commands import stage as stage_command, status as status_command, publish as publish_command

from PLM.api import __version__


VERSION = 'changes {}'.format(__version__)


@contextlib.contextmanager
def work_in(dirname=None):
    """
    Context manager version of os.chdir. When exited, returns to the working
    directory prior to entering.
    """
    curdir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)

        requests_cache.configure(expire_after=60 * 10 * 10)
        from PLM.api import initialise

        yield

    finally:
        os.chdir(curdir)


def print_version(context, param, value):
    if not value or context.resilient_parsing:
        return

    click.echo(VERSION)
    context.exit()


@click.option('--dry-run', help='Prints (instead of executing) the operations to be performed.', is_flag=True, default=False,)
@click.option('--verbose', help='Enables verbose output.', is_flag=True, default=False)
@click.version_option(__version__, '-V', '--version', message=VERSION)
@click.group(context_settings=dict(help_option_names=[u'-h', u'--help']))
def main(dry_run, verbose):
    """Ch-ch-changes"""


@click.command()
@click.argument('repo_directory', required=False)
def status(repo_directory):
    """
    Shows current project release status.
    """
    repo_directory = repo_directory if repo_directory else '.'

    with work_in(repo_directory):
        status_command.status()


main.add_command(status)


@click.command()
@click.option('--draft', help='Enables verbose output.', is_flag=True, default=False)
@click.option('--discard', help='Discards the changes made to release files', is_flag=True, default=False, )
@click.argument('repo_directory', default='.', required=False)
@click.argument('release_name', required=False)
@click.argument('release_description', required=False)
def stage(draft, discard, repo_directory, release_name, release_description):
    """
    Stages a release
    """
    with work_in(repo_directory):
        if discard:
            stage_command.discard(release_name, release_description)
        else:
            stage_command.stage(draft, release_name, release_description)


main.add_command(stage)


@click.command()
@click.argument('repo_directory', default='.', required=False)
def publish(repo_directory):
    """
    Publishes a release
    """
    with work_in(repo_directory):
        publish_command.publish()


main.add_command(publish)


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
