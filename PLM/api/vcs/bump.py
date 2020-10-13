# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import semantic_version, attr, click, re, textwrap
from configparser import RawConfigParser
import ast, tempfile
from pathlib import Path
from plumbum.cmd import diff


from bin.loggers import DamgLogger
from PLM import APP_LOG
logger = DamgLogger(__file__, filepth=APP_LOG)


@attr.s
class BumpVersion(object):

    current_version = attr.ib()

    version_files_to_replace = attr.ib(default=attr.Factory(list))

    @classmethod
    def load(cls, latest_version):

        # TODO: look in other supported bumpversion config locations
        bumpversion = None
        bumpversion_config_path = Path('.bumpversion.cfg')

        if not bumpversion_config_path.exists():
            user_supplied_versioned_file_paths = []

            version_file_path_answer = None
            input_terminator = '.'
            while not version_file_path_answer == input_terminator:

                version_file_path_answer = click.prompt(
                    'Enter a path to a file that contains a version number '
                    "(enter a path of '.' when you're done selecting files)",
                    type=click.Path(exists=True, dir_okay=True, file_okay=True, readable=True),)

                if version_file_path_answer != input_terminator:
                    user_supplied_versioned_file_paths.append(version_file_path_answer)

            bumpversion = cls(
                current_version=latest_version,
                version_files_to_replace=user_supplied_versioned_file_paths,
            )
            bumpversion.write_to_file(bumpversion_config_path)

        return bumpversion

    @classmethod
    def read_from_file(cls, config_path: Path):
        config = RawConfigParser('')
        config.readfp(config_path.open('rt', encoding='utf-8'))

        current_version = config.get("bumpversion", 'current_version')

        filenames = []
        for section_name in config.sections():

            section_name_match = re.compile("^bumpversion:(file|part):(.+)").match(
                section_name
            )

            if not section_name_match:
                continue

            section_prefix, section_value = section_name_match.groups()

            if section_prefix == "file":
                filenames.append(section_value)

        return cls(current_version=current_version, version_files_to_replace=filenames)

    @classmethod
    def write_to_file(self, config_path: Path):
        bumpversion_cfg = textwrap.dedent(
            """\
            [bumpversion]
            current_version = {current_version}
            """
        ).format(**attr.asdict(self))

        bumpversion_files = '\n\n'.join(
            [
                '[bumpversion:file:{}]'.format(file_name)
                for file_name in self.version_files_to_replace
            ]
        )

        config_path.write_text(bumpversion_cfg + bumpversion_files)

    @classmethod
    def current_version(self, module_name):
        return extract_attribute(module_name, '__version__')


    @classmethod
    def get_new_version(self, module_name, current_version, no_input, major=False, minor=False, patch=False):
        proposed_new_version = self.increment(current_version, major=major, minor=minor, patch=patch)
        if no_input:
            new_version = proposed_new_version
        else:
            new_version = click.prompt('What is the release version for "{0}" '.format(module_name),
                                       default=proposed_new_version, )
        return new_version.strip()

    @classmethod
    def increment(self, version, major=False, minor=False, patch=True):
        """
        Increment a semantic version
        :param version: str of the version to increment
        :param major: bool specifying major level version increment
        :param minor: bool specifying minor level version increment
        :param patch: bool specifying patch level version increment
        :return: str of the incremented version
        """
        version = semantic_version.Version(version)
        if major:
            version.major += 1
            version.minor = 0
            version.patch = 0
        elif minor:
            version.minor += 1
            version.patch = 0
        elif patch:
            version.patch += 1

        return str(version)

    @classmethod
    def increment_version(self, context):
        """Increments the __version__ attribute of your module's __init__."""

        replace_attribute(context.module_name, '__version__', context.new_version, dry_run=context.dry_run)

        logger.info('Bumped version from %s to %s' % (context.current_version, context.new_version))



# TODO: leverage bumpversion
def extract_attribute(module_name, attribute_name):
    """Extract metatdata property from a module"""
    with open('%s/__init__.py' % module_name) as input_file:
        for line in input_file:
            if line.startswith(attribute_name):
                return ast.literal_eval(line.split('=')[1].strip())



def replace_attribute(module_name, attribute_name, new_value, dry_run=True):
    """Update a metadata attribute"""
    init_file = '%s/__init__.py' % module_name
    _, tmp_file = tempfile.mkstemp()

    with open(init_file) as input_file:
        with open(tmp_file, 'w') as output_file:
            for line in input_file:
                if line.startswith(attribute_name):
                    line = "%s = '%s'\n" % (attribute_name, new_value)

                output_file.write(line)

    if not dry_run:
        Path(tmp_file).copy(init_file)
    else:
        logger.info(diff(tmp_file, init_file, retcode=None))



def has_attribute(module_name, attribute_name):
    """Is this attribute present?"""
    init_file = '%s/__init__.py' % module_name
    return any([attribute_name in init_line for init_line in open(init_file).readlines()])


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
