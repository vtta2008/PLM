# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------

import io, click, requests
from uritemplate import expand

from PLM.options import EXT_TO_MIME_TYPE
from .bump import BumpVersion, has_attribute, extract_attribute, replace_attribute
from .git import GitHubRepository, git, git_lines, GitHub, Repository

from .repository import (settings, project_settings, initialise, release_from_pull_requests, determine_release,
                         choose_labels, create_venv, write_new_changelog, )


def create_github_release(context, gh_token, description):
    params = {'tag_name': context.new_version, 'name': description, 'body': ''.join(context.changelog_content),
              'prerelease': True, }

    response = requests.post('https://api.github.com/repos/{owner}/{repo}/releases'.format(owner=context.owner,
                                                                                           repo=context.repo),
                             auth=(gh_token, 'x-oauth-basic'), json=params, ).json()

    click.echo('Created release {response}'.format(response=response))

    return response['upload_url']


def upload_release_distributions(context, gh_token, distributions, upload_url):
    for distribution in distributions:
        click.echo('Uploading {distribution} to {upload_url}'.format(distribution=distribution,
                                                                     upload_url=upload_url))

        response = requests.post(expand(upload_url, dict(name=distribution.name)), auth=(gh_token, 'x-oauth-basic'),
                                 headers={'content-type': EXT_TO_MIME_TYPE[distribution.ext]},
                                 data=io.open(distribution, mode='rb'),
                                 verify=False, )

        click.echo('Upload response: {response}'.format(response=response))



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
