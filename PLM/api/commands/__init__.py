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

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
