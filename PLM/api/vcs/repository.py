# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
from collections import OrderedDict
import attr, re, io, os, tempfile, click
from enum import Enum

from plumbum import local
from pathlib import Path
from datetime import date

from PLM.api import note, error, info
from .bump import BumpVersion
from .git import git, GitHubRepository
from bin.loggers import DamgLogger
from PLM import APP_LOG
logger = DamgLogger(__file__, filepth=APP_LOG)




def install(package_name, venv_dir):
    if not os.path.exists(venv_dir):

        venv_dir = create_venv()

    pip = '%s/bin/pip' % venv_dir

    local[pip]('install', package_name)



def publish():

    repository = project_settings.repository

    release = release_from_pull_requests()

    if release.version == str(repository.latest_version):
        info('No staged release to publish')
        return

    info('Publishing release {}'.format(release.version))

    files_to_add = BumpVersion.read_from_file(
        Path('.bumpversion.cfg')
    ).version_files_to_replace
    files_to_add += ['.bumpversion.cfg', str(release.release_file_path)]

    info('Running: git add {}'.format(' '.join(files_to_add)))
    repository.add(files_to_add)

    commit_message = release.release_file_path.read_text(encoding='utf-8')
    info('Running: git commit --message="{}"'.format(commit_message))
    repository.commit(commit_message)

    info('Running: git tag {}'.format(release.version))
    repository.tag(release.version)

    if click.confirm('Happy to publish release {}'.format(release.version)):
        info('Running: git push --tags')
        repository.push()

        info('Creating GitHub Release')
        repository.create_release(release)

        info('Published release {}'.format(release.version))



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



settings = None


project_settings = None


def initialise(project):
    """
    Detects, prompts and initialises the project.
    Stores project and tool configuration in the `changes` module.
    """
    global settings, project_settings

    # Global changes settings
    settings = project.load()

    # Project specific settings
    project_settings = project.load(GitHubRepository(auth_token=settings.auth_token))


def release_from_pull_requests(project):
    project_settings = project.project_settings

    repository = project_settings.repository

    pull_requests = repository.pull_requests_since_latest_version

    labels = set(
        [
            label_name
            for pull_request in pull_requests
            for label_name in pull_request.label_names
        ]
    )

    descriptions = [
        '\n'.join([pull_request.title, pull_request.description])
        for pull_request in pull_requests
    ]

    bumpversion_part, release_type, proposed_version = determine_release(
        repository.latest_version, descriptions, labels
    )

    releases_directory = Path(project_settings.releases_directory)
    if not releases_directory.exists():
        releases_directory.mkdir(parents=True)

    release = Release(release_date=date.today().isoformat(), version=str(proposed_version), bumpversion_part=bumpversion_part,
                        release_type=release_type, )

    release_files = [release_file for release_file in releases_directory.glob('*.md')]
    if release_files:
        release_file = release_files[0]
        release.release_file_path = Path(project_settings.releases_directory).joinpath(
            release_file.name
        )
        release.description = release_file.read_text()

    return release


def determine_release(latest_version, descriptions, labels):
    if 'BREAKING CHANGE' in descriptions:
        return 'major', ReleaseType.BREAKING_CHANGE, latest_version.next_major()
    elif 'enhancement' in labels:
        return 'minor', ReleaseType.FEATURE, latest_version.next_minor()
    elif 'bug' in labels:
        return 'patch', ReleaseType.FIX, latest_version.next_patch()
    else:
        return None, ReleaseType.NO_CHANGE, latest_version


def choose_labels(alternatives):
    """
    Prompt the user select several labels from the provided alternatives.
    At least one label must be selected.
    :param list alternatives: Sequence of options that are available to select from
    :return: Several selected labels
    """
    if not alternatives:
        raise ValueError

    if not isinstance(alternatives, list):
        raise TypeError

    choice_map = OrderedDict(
        ('{}'.format(i), value) for i, value in enumerate(alternatives, 1)
    )
    # prepend a termination option
    input_terminator = '0'
    choice_map.update({input_terminator: '<done>'})
    choice_map.move_to_end('0', last=False)

    choice_indexes = choice_map.keys()

    choice_lines = ['{} - {}'.format(*c) for c in choice_map.items()]
    prompt = '\n'.join(
        (
            'Select labels:',
            '\n'.join(choice_lines),
            'Choose from {}'.format(', '.join(choice_indexes)),
        )
    )

    user_choices = set()
    user_choice = None

    while not user_choice == input_terminator:
        if user_choices:
            note('Selected labels: [{}]'.format(', '.join(user_choices)))

        user_choice = click.prompt(
            prompt, type=click.Choice(choice_indexes), default=input_terminator
        )
        done = user_choice == input_terminator
        new_selection = user_choice not in user_choices
        nothing_selected = not user_choices

        if not done and new_selection:
            user_choices.add(choice_map[user_choice])

        if done and nothing_selected:
            error('Please select at least one label')
            user_choice = None

    return user_choices


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
