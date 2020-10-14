# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
import click, attr
import pkg_resources
from jinja2 import Template
import difflib
from pathlib import Path
import bumpversion

from PLM.api.configs import highlight, note, STYLES, debug, error, info

from PLM.api.vcs import BumpVersion, project_settings, release_from_pull_requests

import logging
from enum import Enum
log = logging.getLogger(__name__)



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


@attr.s
class PullRequest(object):

    number = attr.ib()
    title = attr.ib()
    description = attr.ib()
    author = attr.ib()
    body = attr.ib()
    user = attr.ib()
    labels = attr.ib(default=attr.Factory(list))

    @property
    def description(self):
        return self.body

    @property
    def author(self):
        return self.user['login']

    @property
    def label_names(self):
        return [label['name'] for label in self.labels]

    @classmethod
    def from_github(cls, api_response):
        return cls(**{k.name: api_response[k.name] for k in attr.fields(cls)})

    @classmethod
    def from_number(cls, number):
        pass


class ReleaseType(str, Enum):

    NO_CHANGE = 'no-changes'
    BREAKING_CHANGE = 'breaking'
    FEATURE = 'feature'
    FIX = 'fix'


@attr.s
class Release(object):

    release_date        = attr.ib()
    version             = attr.ib()
    description         = attr.ib(default=attr.Factory(str))
    name                = attr.ib(default=attr.Factory(str))
    notes               = attr.ib(default=attr.Factory(dict))
    release_file_path   = attr.ib(default='')
    bumpversion_part    = attr.ib(default=None)
    release_type        = attr.ib(default=None)

    @property
    def title(self):
        return '{version} ({release_date})'.format(version=self.version, release_date=self.release_date) + ((' ' + self.name) if self.name else '')

    @property
    def release_note_filename(self):
        return '{version}-{release_date}'.format(version=self.version, release_date=self.release_date) + (('-' + self.name) if self.name else '')

    @classmethod
    def generate_notes(cls, project_labels, pull_requests_since_latest_version):
        for label, properties in project_labels.items():

            pull_requests_with_label = [pull_request for pull_request in pull_requests_since_latest_version
                if label in pull_request.label_names]

            project_labels[label]['pull_requests'] = pull_requests_with_label

        return project_labels



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
