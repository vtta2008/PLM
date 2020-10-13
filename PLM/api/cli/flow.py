# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
import logging

import click
import pkg_resources
from jinja2 import Template
import difflib
from pathlib import Path
import bumpversion
from PLM.api.models import generate_changelog
from PLM.api.config import project_config, store_settings
from .packaging import ( build_distributions, install_from_pypi, install_package, upload_package,)
from PLM.api.vcs import (create_github_release, upload_release_distributions, BumpVersion, project_settings,
                         release_from_pull_requests)
from PLM.api.inspect import highlight, note, STYLES, debug, error, info, run_tests
from .packaging import tag_and_push, commit_version_change
log = logging.getLogger(__name__)


def publish(context):
    """Publishes the project"""
    commit_version_change(context)

    if context.github:
        # github token
        project_settings = project_config(context.module_name)
        if not project_settings['gh_token']:
            click.echo('You need a GitHub token for changes to create a release.')
            click.pause(
                'Press [enter] to launch the GitHub "New personal access '
                'token" page, to create a token for changes.'
            )
            click.launch('https://github.com/settings/tokens/new')
            project_settings['gh_token'] = click.prompt('Enter your changes token')

            store_settings(context.module_name, project_settings)
        description = click.prompt('Describe this release')

        upload_url = create_github_release(
            context, project_settings['gh_token'], description
        )

        upload_release_distributions(
            context,
            project_settings['gh_token'],
            build_distributions(context),
            upload_url,
        )

        click.pause('Press [enter] to review and update your new release')
        click.launch(
            '{0}/releases/tag/{1}'.format(context.repo_url, context.new_version)
        )
    else:
        tag_and_push(context)


def perform_release(context):
    """Executes the release process."""
    try:
        run_tests()

        if not context.skip_changelog:
            generate_changelog(context)

        BumpVersion.increment_version(context)

        build_distributions(context)

        install_package(context)

        upload_package(context)

        install_from_pypi(context)

        publish(context)
    except Exception:
        log.exception('Error releasing')


def status():

    repository = project_settings.repository

    release = release_from_pull_requests()

    info('Status [{}/{}]'.format(repository.owner, repository.repo))

    info('Repository: ' + highlight('{}/{}'.format(repository.owner, repository.repo)))

    info('Latest Version')
    note(repository.latest_version)

    info('Changes')
    unreleased_changes = repository.pull_requests_since_latest_version
    note(
        '{} changes found since {}'.format(
            len(unreleased_changes), repository.latest_version
        )
    )

    for pull_request in unreleased_changes:
        note(
            '#{} {} by @{}{}'.format(
                pull_request.number,
                pull_request.title,
                pull_request.author,
                ' [{}]'.format(','.join(pull_request.label_names))
                if pull_request.label_names
                else '',
            )
        )

    if unreleased_changes:
        info(
            'Computed release type {} from changes issue tags'.format(
                release.release_type
            )
        )
        info(
            'Proposed version bump {} => {}'.format(
                repository.latest_version, release.version
            )
        )


def discard(release_name='', release_description=''):

    repository = project_settings.repository

    release = release_from_pull_requests()

    if release.version == str(repository.latest_version):
        info('No staged release to discard')
        return

    info('Discarding currently staged release {}'.format(release.version))

    bumpversion = BumpVersion.read_from_file(Path('.bumpversion.cfg'))
    git_discard_files = bumpversion.version_files_to_replace + [
        # 'CHANGELOG.md',
        '.bumpversion.cfg'
    ]

    info('Running: git {}'.format(' '.join(['checkout', '--'] + git_discard_files)))
    repository.discard(git_discard_files)

    if release.release_file_path.exists():
        info('Running: rm {}'.format(release.release_file_path))
        release.release_file_path.unlink()


def stage(draft, release_name='', release_description=''):

    repository = project_settings.repository

    release = release_from_pull_requests()
    release.name = release_name
    release.description = release_description

    if not repository.pull_requests_since_latest_version:
        error("There aren't any changes to release since {}".format(release.version))
        return

    info(
        'Staging [{}] release for version {}'.format(
            release.release_type, release.version
        )
    )

    # Bumping versions
    if BumpVersion.read_from_file(Path('.bumpversion.cfg')).current_version == str(
        release.version
    ):
        info('Version already bumped to {}'.format(release.version))
    else:
        bumpversion_arguments = (
            BumpVersion.DRAFT_OPTIONS if draft else BumpVersion.STAGE_OPTIONS
        ) + [release.bumpversion_part]

        info('Running: bumpversion {}'.format(' '.join(bumpversion_arguments)))
        bumpversion.main(bumpversion_arguments)

    # Release notes generation
    info('Generating Release')
    release.notes = Release.generate_notes(
        project_settings.labels, repository.pull_requests_since_latest_version
    )

    # TODO: if project_settings.release_notes_template is None
    release_notes_template = pkg_resources.resource_string(
        __name__, 'templates/release_notes_template.md'
    ).decode('utf8')

    release_notes = Template(release_notes_template).render(release=release)

    releases_directory = Path(project_settings.releases_directory)
    if not releases_directory.exists():
        releases_directory.mkdir(parents=True)

    release_notes_path = releases_directory.joinpath(
        '{}.md'.format(release.release_note_filename)
    )

    if draft:
        info('Would have created {}:'.format(release_notes_path))
        debug(release_notes)
    else:
        info('Writing release notes to {}'.format(release_notes_path))
        if release_notes_path.exists():
            release_notes_content = release_notes_path.read_text(encoding='utf-8')
            if release_notes_content != release_notes:
                info(
                    '\n'.join(
                        difflib.unified_diff(
                            release_notes_content.splitlines(),
                            release_notes.splitlines(),
                            fromfile=str(release_notes_path),
                            tofile=str(release_notes_path),
                        )
                    )
                )
                if click.confirm(
                    click.style(
                        '{} has modified content, overwrite?'.format(
                            release_notes_path
                        ),
                        **STYLES['error']
                    )
                ):
                    release_notes_path.write_text(release_notes, encoding='utf-8')
        else:
            release_notes_path.write_text(release_notes, encoding='utf-8')
# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
