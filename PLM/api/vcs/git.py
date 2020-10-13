# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
from pathlib import Path
import cached_property
from plumbum.cmd import git as git_command
import shlex
import attr, requests, uritemplate, giturlparse, semantic_version
from PLM.options import (GITHUB_MERGED_PULL_REQUEST, EXT_TO_MIME_TYPE, IS_WINDOWS, ISSUE_ENDPOINT, LABELS_ENDPOINT,
                         RELEASES_ENDPOINT)


def git(command):
    command = shlex.split(command, posix=not IS_WINDOWS)
    return git_command[command]()


def git_lines(command):
    return git(command).splitlines()


@attr.s
class GitHub(object):

    repository = attr.ib()

    @property
    def owner(self):
        return self.repository.owner

    @property
    def repo(self):
        return self.repository.repo

    @property
    def auth_token(self):
        return self.repository.auth_token

    @property
    def headers(self):
        # TODO: requests.Session
        return {'Authorization': 'token {}'.format(self.auth_token)}

    def pull_request(self, pr_num):
        pull_request_api_url = uritemplate.expand(ISSUE_ENDPOINT, dict(owner=self.owner, repo=self.repo,
                                                                            number=pr_num))

        return requests.get(pull_request_api_url, headers=self.headers).json()

    def labels(self):
        labels_api_url = uritemplate.expand(LABELS_ENDPOINT, dict(owner=self.owner, repo=self.repo))

        return requests.get(labels_api_url, headers=self.headers).json()

    def create_release(self, release, uploads=None):
        params = {  'tag_name': release.version, 'name': release.name, 'body': release.description, 'prerelease': True,}

        releases_api_url = uritemplate.expand(RELEASES_ENDPOINT, dict(owner=self.owner, repo=self.repo))

        response = requests.post(releases_api_url, headers=self.headers, json=params).json()

        upload_url = response['upload_url']

        upload_responses = ([self.create_upload(upload_url, Path(upload)) for upload in uploads]if uploads else [])

        return response, upload_responses

    def create_upload(self, upload_url, upload_path):
        requests.post(
            uritemplate.expand(upload_url, {'name': upload_path.name}), headers=dict(**self.headers,
                            **{'content-type': EXT_TO_MIME_TYPE[upload_path.ext]}), data=upload_path.read_bytes(),
                            verify=False, )



@attr.s
class Repository(object):

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
class GitHubRepository(Repository):

    api     = attr.ib(default=None)

    def __attrs_post_init__(self):
        self.api = GitHub(self)

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



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
