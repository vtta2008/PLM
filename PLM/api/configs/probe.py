# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
import logging
from os.path import exists

from plumbum import local
from plumbum.cmd import git
from plumbum.commands import CommandNotFound
from PLM.cores.Errors import ProbeException
from PLM.options            import TOOLS, README_EXTENSIONS, TEST_RUNNERS
from PLM.api.vcs            import has_attribute
from .consoles              import dry_run


logger = logging.getLogger(__name__)



def report_and_raise(probe_name, probe_result, failure_msg):
    """Logs the probe result and raises on failure"""
    logger.info('%s? %s' % (probe_name, probe_result))
    if not probe_result:
        raise ProbeException(failure_msg)
    else:
        return True


def has_setup():
    """`setup.py`"""
    return report_and_raise(
        'Has a setup.py', exists('setup.py'), 'Your project needs a setup.py'
    )


def has_binary(command):
    try:
        local.which(command)
        return True
    except CommandNotFound:
        logger.info('%s does not exist' % command)
        return False


def has_tools():
    return any([has_binary(tool) for tool in TOOLS])


def has_test_runner():
    return any([has_binary(runner) for runner in TEST_RUNNERS])


def has_changelog():
    """CHANGELOG.md"""
    return report_and_raise(
        'CHANGELOG.md', exists('CHANGELOG.md'), 'Create a CHANGELOG.md file'
    )


def has_readme():
    """README"""
    return report_and_raise(
        'README',
        any([exists('README{}'.format(ext)) for ext in README_EXTENSIONS]),
        'Create a (valid) README',
    )


def has_metadata(python_module):
    """`<module_name>/__init__.py` with `__version__` and `__url__`"""
    init_path = '{}/__init__.py'.format(python_module)
    has_metadata = (
        exists(init_path)
        and has_attribute(python_module, '__version__')
        and has_attribute(python_module, '__url__')
    )
    return report_and_raise('Has module metadata', has_metadata,
        'Your %s/__init__.py must contain __version__ and __url__ attributes',)


def has_signing_key(context):
    return 'signingkey' in git('config', '-l')


def probe_project(python_module):
    """
    Check if the project meets `changes` requirements.
    Complain and exit otherwise.
    """
    logger.info('Checking project for changes requirements.')
    return (
        has_tools()
        and has_setup()
        and has_metadata(python_module)
        and has_test_runner()
        and has_readme()
        and has_changelog()
    )


def get_test_runner():
    test_runners = ['tox', 'nosetests', 'py.test']
    test_runner = None
    for runner in test_runners:
        try:
            test_runner = local[runner]
        except CommandNotFound:
            continue
    return test_runner


def run_tests():
    """Executes your tests."""
    test_runner = get_test_runner()
    if test_runner:
        result = test_runner()
        logger.info('Test execution returned:\n%s' % result)
        return result
    else:
        logger.info('No test runner found')

    return None


def run_test_command(context):
    if context.test_command:
        result = dry_run(context.test_command, context.dry_run)
        logger.info('Test command "%s", returned %s', context.test_command, result)
    return True


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
