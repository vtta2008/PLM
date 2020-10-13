# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
import shlex

import giturlparse
import semantic_version
from cached_property import cached_property
from plumbum.cmd import git as git_command


import attr, re, io

from enum import Enum
from bin.loggers import DamgLogger
from PLM import APP_LOG
logger = DamgLogger(__file__, filepth=APP_LOG)
from PLM.api.models import services
from PLM.api.version import IS_WINDOWS


GITHUB_MERGED_PULL_REQUEST = re.compile(r'^([0-9a-f]{5,40}) Merge pull request #(\w+)')


def git(command):
    command = shlex.split(command, posix=not IS_WINDOWS)
    return git_command[command]()


def git_lines(command):
    return git(command).splitlines()


@attr.s
class GitRepository(object):

    VERSION_ZERO = semantic_version.Version('0.0.0')


    # TODO: handle multiple remotes (for non-owner maintainer workflows)
    REMOTE_NAME = 'origin'


    auth_token = attr.ib(default=None)

    @property
    def remote_url(self):
        return git('config --get remote.{}.url'.format(self.REMOTE_NAME))

    @property
    def parsed_repo(self):
        return giturlparse.parse(self.remote_url)

    @property
    def repo(self):
        return self.parsed_repo.repo

    @property
    def owner(self):
        return self.parsed_repo.owner

    @property
    def platform(self):
        return self.parsed_repo.platform

    @property
    def is_github(self):
        return self.parsed_repo.github

    @property
    def is_bitbucket(self):
        return self.parsed_repo.bitbucket

    @property
    def commit_history(self):
        return [commit_message for commit_message in git_lines('logger --oneline --no-color') if commit_message]

    @property
    def first_commit_sha(self):
        return git('rev-list --max-parents=0 HEAD')

    @property
    def tags(self):
        return git_lines('tag --list')

    @property
    def versions(self):
        versions = []
        for tag in self.tags:
            try:
                versions.append(semantic_version.Version(tag))
            except ValueError:
                pass
        return versions

    @property
    def latest_version(self) -> semantic_version.Version:
        return max(self.versions) if self.versions else self.VERSION_ZERO

    def merges_since(self, version=None):
        if version == semantic_version.Version('0.0.0'):
            version = self.first_commit_sha

        revision_range = ' {}..HEAD'.format(version) if version else ''

        merge_commits = git(
            'logger --oneline --merges --no-color{}'.format(revision_range)
        ).split('\n')
        return merge_commits

    @property
    def merges_since_latest_version(self):
        return self.merges_since(self.latest_version)

    @property
    def files_modified_in_last_commit(self):
        return git('diff --name -only --diff -filter=d')

    @property
    def dirty_files(self):
        return [
            modified_path
            for modified_path in git('-c color.status=false status --short --branch')
            if modified_path.startswith(' M')
        ]

    @staticmethod
    def add(files_to_add):
        return git('add {}'.format(' '.join(files_to_add)))

    @staticmethod
    def commit(message):
        # FIXME: message is one token
        return git_command['commit', '--message="{}"'.format(message)]()

    @staticmethod
    def discard(file_paths):
        return git('checkout -- {}'.format(' '.join(file_paths)))

    @staticmethod
    def tag(version):
        # TODO: signed tags
        return git(
            'tag --annotate {version} --message="{version}"'.format(version=version)
        )

    @staticmethod
    def push():
        return git('push --tags')


@attr.s
class GitHubRepository(GitRepository):

    api     = attr.ib(default=None)

    def __attrs_post_init__(self):
        self.api = services.GitHub(self)

    @cached_property
    def labels(self):
        return self.api.labels()

    @cached_property
    def pull_requests_since_latest_version(self):
        return [PullRequest.from_github(self.api.pull_request(pull_request_number))
            for pull_request_number in self.pull_request_numbers_since_latest_version]

    @property
    def pull_request_numbers_since_latest_version(self):
        pull_request_numbers = []

        for commit_msg in self.merges_since(self.latest_version):

            matches = GITHUB_MERGED_PULL_REQUEST.findall(commit_msg)

            if matches:
                _, pull_request_number = matches[0]
                pull_request_numbers.append(pull_request_number)

        return pull_request_numbers

    def create_release(self, release):
        return self.api.create_release(release)



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



def write_new_changelog(repo_url, filename, content_lines, dry_run=True):
    heading_and_newline = '# [Changelog](%s/releases)\n' % repo_url

    with io.open(filename, 'r+') as f:
        existing = f.readlines()

    output = existing[2:]
    output.insert(0, '\n')

    for index, line in enumerate(content_lines):
        output.insert(0, content_lines[len(content_lines) - index - 1])

    output.insert(0, heading_and_newline)

    output = ''.join(output)

    if not dry_run:
        with io.open(filename, 'w+') as f:
            f.write(output)
    else:
        logger.info('New changelog:\n%s', ''.join(content_lines))



def replace_sha_with_commit_link(repo_url, git_log_content):
    git_log_content = git_log_content.split('\n')
    for index, line in enumerate(git_log_content):
        # http://stackoverflow.com/a/468378/5549
        sha1_re = re.match(r'^[0-9a-f]{5,40}\b', line)
        if sha1_re:
            sha1 = sha1_re.group()

            new_line = line.replace(sha1, '[%s](%s/commit/%s)' % (sha1, repo_url, sha1))
            logger.debug('old line: %s\nnew line: %s', line, new_line)
            git_log_content[index] = new_line

    return git_log_content



def generate_changelog(context):
    """Generates an automatic changelog from your commit messages."""

    changelog_content = [
        '\n## [%s](%s/compare/%s...%s)\n\n'
        % (
            context.new_version,
            context.repo_url,
            context.current_version,
            context.new_version,
        )
    ]

    git_log_content = None
    git_log = 'logger --oneline --no-merges --no-color'.split(' ')
    try:
        git_log_tag = git_log + ['%s..master' % context.current_version]
        git_log_content = git(git_log_tag)
        logger.debug('content: %s' % git_log_content)
    except Exception:
        logger.warn('Error diffing previous version, initial release')
        git_log_content = git(git_log)

    git_log_content = replace_sha_with_commit_link(context.repo_url, git_log_content)
    # turn change logger entries into markdown bullet points
    if git_log_content:
        [
            changelog_content.append('* %s\n' % line) if line else line
            for line in git_log_content[:-1]
        ]

    write_new_changelog(
        context.repo_url, 'CHANGLOG.md', changelog_content, dry_run=context.dry_run
    )
    logger.info('Added content to CHANGELOG.md')
    context.changelog_content = changelog_content




# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
