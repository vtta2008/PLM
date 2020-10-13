# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
import click

STYLES = {
    'debug': {'fg': 'blue'},
    'info': {'fg': 'green', 'bold': True},
    'highlight': {'fg': 'cyan', 'bold': True},
    'note': {'fg': 'blue', 'bold': True},
    'error': {'fg': 'red', 'bold': True},
}


def echo(message, style):
    click.secho(str(message), **STYLES[style])


def debug(message):
    echo('{}...'.format(message), 'debug')


def info(message):
    echo('{}...'.format(message), 'info')


def note(message):
    echo(message, 'note')


def note_style(message):
    return click.style(message, **STYLES['note'])


def highlight(message):
    return click.style(message, **STYLES['highlight'])


def error(message):
    echo(message, 'error')


from .probe import (report_and_raise, has_setup, has_tools, has_binary, has_readme, has_metadata, has_signing_key,
                    probe_project, has_changelog, has_test_runner, has_tools, has_binary)

from .stage import discard, status, stage


from .verification import run_tests, run_test_command, get_test_runner, get_test_runner



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
