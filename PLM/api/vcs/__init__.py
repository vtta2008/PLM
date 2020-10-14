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
                         choose_labels, write_new_changelog, generate_changelog, replace_sha_with_commit_link,
                         install)




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
