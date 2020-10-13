# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
import logging
from pathlib import Path
from shutil import rmtree
from PLM.options import COMMIT_TEMPLATE, TAG_TEMPLATE
from plumbum import local
from PLM.utils import mktmpdir
from PLM.api.inspect import run_test_command, has_signing_key
from PLM.api.models import create_venv, install
log = logging.getLogger(__name__)


def commit_version_change(context):
    # TODO: signed commits?
    dry_run(COMMIT_TEMPLATE % (context.new_version, context.module_name), context.dry_run)
    dry_run('git push', context.dry_run)


def tag_and_push(context):
    """Tags your git repo with the new version number"""

    tag_option = '--annotate'
    if has_signing_key(context):
        tag_option = '--sign'

    dry_run(TAG_TEMPLATE % (tag_option, context.new_version, context.new_version), context.dry_run, )
    dry_run('git push --tags', context.dry_run)


def build_distributions(context):
    """Builds package distributions"""

    rmtree('dist', ignore_errors=True)

    build_package_command   = 'python setup.py clean sdist bdist_wheel'
    result                  = dry_run(build_package_command, context.dry_run)
    packages                = Path('dist').files() if not context.dry_run else "nothing"

    if not result:
        raise Exception('Error building packages: %s' % result)
    else:
        log.info('Built %s' % ', '.join(packages))

    return packages


# tox
def install_package(context):
    """Attempts to install the sdist and wheel."""

    if not context.dry_run and build_distributions(context):
        with mktmpdir() as tmp_dir:
            create_venv(tmp_dir=tmp_dir)
            for distribution in Path('dist').files():
                try:
                    install(distribution, tmp_dir)
                    log.info('Successfully installed %s', distribution)
                    if context.test_command and run_test_command(context):
                        log.info(
                            'Successfully ran test command: %s', context.test_command
                        )
                except Exception as e:
                    raise Exception(
                        'Error installing distribution %s' % distribution, e
                    )
    else:
        log.info('Dry run, skipping installation')


# twine
def upload_package(context):
    """Uploads your project packages to pypi with twine."""

    if not context.dry_run and build_distributions(context):
        upload_args = 'twine upload '
        upload_args += ' '.join(Path('dist').files())
        if context.pypi:
            upload_args += ' -r %s' % context.pypi

        upload_result = dry_run(upload_args, context.dry_run)
        if not context.dry_run and not upload_result:
            raise Exception('Error uploading: %s' % upload_result)
        else:
            log.info(
                'Successfully uploaded %s:%s', context.module_name, context.new_version
            )
    else:
        log.info('Dry run, skipping package upload')


def install_from_pypi(context):
    """Attempts to install your package from pypi."""

    tmp_dir = create_venv()
    install_cmd = '%s/bin/pip install %s' % (tmp_dir, context.module_name)

    package_index = 'pypi'
    if context.pypi:
        install_cmd += '-i %s' % context.pypi
        package_index = context.pypi

    try:
        result = dry_run(install_cmd, context.dry_run)
        if not context.dry_run and not result:
            log.error(
                'Failed to install %s from %s', context.module_name, package_index
            )
        else:
            log.info(
                'Successfully installed %s from %s', context.module_name, package_index
            )

    except Exception as e:
        error_msg = 'Error installing %s from %s' % (context.module_name, package_index)
        log.exception(error_msg)
        raise Exception(error_msg, e)


def dry_run(command, dry_run):
    """Executes a shell command unless the dry run option is set"""
    if not dry_run:
        cmd_parts = command.split(' ')
        # http://plumbum.readthedocs.org/en/latest/local_commands.html#run-and-popen
        return local[cmd_parts[0]](cmd_parts[1:])
    else:
        log.info('Dry run of %s, skipping' % command)
    return True



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
