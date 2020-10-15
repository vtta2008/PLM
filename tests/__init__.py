# -*- coding: utf-8 -*-
"""

Script Name: __init__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

    In this directory resides our test suite. I'm not gonna go into too much detail here as we will dedicate whole
    section to testing, but just briefly:

    1. test_app.py is a test file corresponding to app.py in source directory
    2. conftest.py is probably familiar to you if you ever used Pytest - it's a file used for specifying Pytest
        fixtures, hooks or loading external plugins.
    3. context.py helps with imports of source code files from blueprint directory by manipulating class path.
        We will see how that works in sec.

"""
# -------------------------------------------------------------------------------------------------------------

fmtInfo = """
<valid semver> ::= <version core>
                 | <version core> "-" <pre-release>
                 | <version core> "+" <build>
                 | <version core> "-" <pre-release> "+" <build>

<version core> ::= <major> "." <minor> "." <patch>

<major> ::= <numeric identifier>

<minor> ::= <numeric identifier>

<patch> ::= <numeric identifier>

<pre-release> ::= <dot-separated pre-release identifiers>

<dot-separated pre-release identifiers> ::= <pre-release identifier>
                                          | <pre-release identifier> "." <dot-separated pre-release identifiers>

<build> ::= <dot-separated build identifiers>

<dot-separated build identifiers> ::= <build identifier>
                                    | <build identifier> "." <dot-separated build identifiers>

"""

docInfo = """ 

In the world of software management there exists a dreaded place called “dependency hell.” The bigger your system grows 
and the more packages you integrate into your software, the more likely you are to find yourself, one day, in this pit 
of despair.

In systems with many dependencies, releasing new package versions can quickly become a nightmare. If the dependency 
specifications are too tight, you are in danger of version lock (the inability to upgrade a package without having to 
release new versions of every dependent package). If dependencies are specified too loosely, you will inevitably be 
bitten by version promiscuity (assuming compatibility with more future versions than is reasonable). Dependency hell 
is where you are when version lock and/or version promiscuity prevent you from easily and safely moving your project 
forward.

As a solution to this problem, I propose a simple set of rules and requirements that dictate how version numbers are 
assigned and incremented. These rules are based on but not necessarily limited to pre-existing widespread common 
practices in use in both closed and open-source software. For this system to work, you first need to declare a public 
API. This may consist of documentation or be enforced by the code itself. Regardless, it is important that this API be 
clear and precise. Once you identify your public API, you communicate changes to it with specific increments to your 
version number. Consider a version format of X.Y.Z (Major.Minor.Patch). Bug fixes not affecting the API increment the 
patch version, backwards compatible API additions/changes increment the minor version, and backwards incompatible API 
changes increment the major version.

I call this system “Semantic Versioning.” Under this scheme, version numbers and the way they change convey meaning 
about the underlying code and what has been modified from one version to the next.

 """


import re
import functools

class Max(object):
    __slots__ = []

    def __repr__(self):
        return 'Max()'

    def __eq__(self, other):
        return isinstance(other, self.__class__)


@functools.total_ordering
class Numeric(object):

    __slots__ = ['value']

    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return 'Numeric(%r)' % self.value

    def __eq__(self, other):
        if isinstance(other, Numeric):
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Max):
            return True
        elif isinstance(other, Alpha):
            return True
        elif isinstance(other, Numeric):
            return self.value < other.value
        else:
            return NotImplemented


@functools.total_ordering
class Alpha(object):

    __slots__ = ['value']

    def __init__(self, value):
        self.value = value.encode('ascii')

    def __repr__(self):
        return 'Alpha(%r)' % self.value

    def __eq__(self, other):
        if isinstance(other, Alpha):
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Max):
            return True
        elif isinstance(other, Numeric):
            return False
        elif isinstance(other, Alpha):
            return self.value < other.value
        else:
            return NotImplemented


class VersionFactory(type):

    __slots__ = ()

    @classmethod
    def __prepare__(mcs, name, bases, meta_args=None, meta_options=None):
        """
        __prepare__ lets you supply a custom mapping (such as an OrderedDict) to be used as the namespace while the
        class is being created. You must return an instance of whatever namespace you choose. If you don't implement
        __prepare__ a normal dict is used.

        meta_args and meta_options is not necessarily needed, just so you know.

        This function will add documents into every version class.

        Example:
            class Version(metaclass=VersionFactory): pass
            version = Version()
            print(version.__doc__)
            print(version.__format__)

        """
        construct = dict()
        construct['__doc__'] = docInfo
        construct['__format__'] = fmtInfo
        return construct

    def __new__(cls, name, bases, construct, meta_args=None, meta_options=None):

        original_getattr = construct.get('__getattribute__')
        original_setattr = construct.get('__setattr__')

        def init_getattr(self, item):
            if original_getattr is not None:
                return original_getattr(self, item)
            else:
                return super(eval(name), self).__getattribute__(item)

        def init_setattr(self, key, value):
            if not key in construct['__slots__']:
                raise AttributeError(f"you can't modify private members:_{0}".format(key))
            if original_setattr is not None:
                original_setattr(self, key, value)
            else:
                super(eval(name), self).__setattr__(key, value)

        construct['__getattribute__'] = init_getattr
        construct['__setattr__'] = init_setattr

        return super().__new__(cls, name, bases, construct)




def _comparable(klass):

    """ C{__eq__}, C{__lt__}, etc. methods are added to the class,
    relying on C{__cmp__} to implement their comparisons. """

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.major == other.major and self.minor == other.minor and self.patch == other.patch
            and (self.prerelease or ()) == (other.prerelease or ()) and (self.build or ()) == (other.build or ())
        )

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return tuple(self) != tuple(other)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.precedence_key < other.precedence_key

    def __le__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.precedence_key <= other.precedence_key

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.precedence_key > other.precedence_key

    def __ge__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.precedence_key >= other.precedence_key

    klass.__eq__ = __eq__
    klass.__lt__ = __lt__
    klass.__gt__ = __gt__
    klass.__le__ = __le__
    klass.__ge__ = __ge__
    klass.__ne__ = __ne__
    return klass


def _has_leading_zero(value):
    return (value and value[0] == '0' and value.isdigit() and value != '0')


@_comparable
class Version(metaclass=VersionFactory):

    """
    with VersionFactory manipulation, you don't have to write as following
    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age
    """

    __slots__ = ('version_string', 'major', 'minor', 'patch', 'prerelease', 'build')

    version_re = re.compile(r'^(\d+)\.(\d+)\.(\d+)(?:-([0-9a-zA-Z.-]+))?(?:\+([0-9a-zA-Z.-]+))?$')
    partial_version_re = re.compile(r'^(\d+)(?:\.(\d+)(?:\.(\d+))?)?(?:-([0-9a-zA-Z.-]*))?(?:\+([0-9a-zA-Z.-]*))?$')

    def __init__(self, version_string=None, major=None, minor=None, patch=None, prerelease=None, build=None):
        if version_string:
            major, minor, patch, prerelease, build = self.parse(version_string)
        else:
            # Convenience: allow to omit prerelease/build.
            prerelease = tuple(prerelease or ())

            build = tuple(build or ())
            self.validate_kwargs(major, minor, patch, prerelease, build)
            self.version_string = version_string

        self.version_string = version_string
        self.major = major
        self.minor = minor
        self.patch = patch
        self.prerelease = prerelease
        self.build = build

    def __getattribute__(self, item):
        """
        is just for IDE recognize.
        """
        return super().__getattribute__(item)

    def __iter__(self):
        return iter((self.major, self.minor, self.patch, self.prerelease, self.build))

    def __str__(self):
        version = '%d' % self.major
        if self.minor is not None:
            version = '%s.%d' % (version, self.minor)
        if self.patch is not None:
            version = '%s.%d' % (version, self.patch)
        if self.prerelease or (self.prerelease == () and self.build is None):
            version = '%s-%s' % (version, '.'.join(self.prerelease))
        if self.build or self.build == ():
            version = '%s+%s' % (version, '.'.join(self.build))
        return version

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, str(self))

    def __hash__(self):
        return hash((self.major, self.minor, self.patch, self.prerelease, self.build))

    @classmethod
    def coerce(cls, version_string):
        """Coerce an arbitrary version string into a semver-compatible one.

        The rule is:
        - If not enough components, fill minor/patch with zeroes; unless
          partial=True
        - If more than 3 dot-separated components, extra components are "build"
          data. If some "build" data already appeared, append it to the
          extra components

        Examples:
            >>> Version.coerce('0.1')
            Version(0, 1, 0)
            >>> Version.coerce('0.1.2.3')
            Version(0, 1, 2, (), ('3',))
            >>> Version.coerce('0.1.2.3+4')
            Version(0, 1, 2, (), ('3', '4'))
            >>> Version.coerce('0.1+2-3+4_5')
            Version(0, 1, 0, (), ('2-3', '4-5'))
        """
        base_re = re.compile(r'^\d+(?:\.\d+(?:\.\d+)?)?')

        match = base_re.match(version_string)
        if not match:
            raise ValueError("Version string lacks a numerical component: %r" % version_string)

        version = version_string[:match.end()]
        # We need a not-partial version.
        while version.count('.') < 2:
            version += '.0'

        # Strip leading zeros in components
        # Version is of the form nn, nn.pp or nn.pp.qq
        # If the part was '0', we end up with an empty string.
        version = '.'.join(part.lstrip('0') or '0' for part in version.split('.'))

        if match.end() == len(version_string):
            return Version(version)

        rest = version_string[match.end():]

        # Cleanup the 'rest'
        rest = re.sub(r'[^a-zA-Z0-9+.-]', '-', rest)

        if rest[0] == '+':
            # A 'build' component
            prerelease = ''
            build = rest[1:]
        elif rest[0] == '.':
            # An extra version component, probably 'build'
            prerelease = ''
            build = rest[1:]
        elif rest[0] == '-':
            rest = rest[1:]
            if '+' in rest:
                prerelease, build = rest.split('+', 1)
            else:
                prerelease, build = rest, ''
        elif '+' in rest:
            prerelease, build = rest.split('+', 1)
        else:
            prerelease, build = rest, ''

        build = build.replace('+', '.')

        if prerelease:
            version = '%s-%s' % (version, prerelease)
        if build:
            version = '%s+%s' % (version, build)

        return cls(version)

    @classmethod
    def parse(cls, version_string):
        """Parse a version string into a Version() object.

        Args:
            version_string (str), the version string to parse
            partial (bool), whether to accept incomplete input
            coerce (bool), whether to try to map the passed in string into a
                valid Version.
        """
        if not version_string:
            raise ValueError('Invalid empty version string: %r' % version_string)

        version_re = cls.version_re

        match = version_re.match(version_string)
        if not match:
            raise ValueError('Invalid version string: %r' % version_string)

        major, minor, patch, prerelease, build = match.groups()

        if _has_leading_zero(major):
            raise ValueError("Invalid leading zero in major: %r" % version_string)
        if _has_leading_zero(minor):
            raise ValueError("Invalid leading zero in minor: %r" % version_string)
        if _has_leading_zero(patch):
            raise ValueError("Invalid leading zero in patch: %r" % version_string)

        major = int(major)
        minor = cls.coerce(minor)
        patch = cls.coerce(patch)

        if prerelease is None:
            if build is None:
                # No build info, strip here
                return (major, minor, patch, None, None)
            else:
                prerelease = ()
        elif prerelease == '':
            prerelease = ()
        else:
            prerelease = tuple(prerelease.split('.'))
            cls.validate_identifiers(prerelease, allow_leading_zeroes=False)

        if build is None:
            build = ()
        elif build == '':
            build = ()
        else:
            build = tuple(build.split('.'))
            cls.validate_identifiers(build, allow_leading_zeroes=True)

        return (major, minor, patch, prerelease, build)

    @property
    def precedence_key(self):
        if self.prerelease:
            prerelease_key = tuple(Numeric(part) if re.match(r'^[0-9]+$', part) else Alpha(part) for part in self.prerelease)
        else:
            prerelease_key = (Max(), )

        return (self.major, self.minor, self.patch, prerelease_key,)

    @classmethod
    def coerce(cls, value, allow_none=False):
        if value is None and allow_none:
            return value
        return int(value)

    @classmethod
    def validate_identifiers(cls, identifiers, allow_leading_zeroes=False):
        for item in identifiers:
            if not item:
                raise ValueError(
                    "Invalid empty identifier %r in %r"
                    % (item, '.'.join(identifiers))
                )

            if item[0] == '0' and item.isdigit() and item != '0' and not allow_leading_zeroes:
                raise ValueError("Invalid leading zero in identifier %r" % item)

    @classmethod
    def validate_kwargs(cls, major, minor, patch, prerelease, build, partial):
        if (
                major != int(major)
                or minor != cls.coerce(minor, partial)
                or patch != cls.coerce(patch, partial)
                or prerelease is None and not partial
                or build is None and not partial
        ):
            raise ValueError(
                "Invalid kwargs to Version(major=%r, minor=%r, patch=%r, "
                "prerelease=%r, build=%r, partial=%r" % (
                    major, minor, patch, prerelease, build, partial
                ))
        if prerelease is not None:
            cls._validate_identifiers(prerelease, allow_leading_zeroes=False)
        if build is not None:
            cls._validate_identifiers(build, allow_leading_zeroes=True)

    @classmethod
    def parse(cls, version_string, partial=False, coerce=False):
        """Parse a version string into a Version() object.

        Args:
            version_string (str), the version string to parse
            partial (bool), whether to accept incomplete input
            coerce (bool), whether to try to map the passed in string into a
                valid Version.
        """
        if not version_string:
            raise ValueError('Invalid empty version string: %r' % version_string)

        if partial:
            version_re = cls.partial_version_re
        else:
            version_re = cls.version_re

        match = version_re.match(version_string)
        if not match:
            raise ValueError('Invalid version string: %r' % version_string)

        major, minor, patch, prerelease, build = match.groups()

        if _has_leading_zero(major):
            raise ValueError("Invalid leading zero in major: %r" % version_string)
        if _has_leading_zero(minor):
            raise ValueError("Invalid leading zero in minor: %r" % version_string)
        if _has_leading_zero(patch):
            raise ValueError("Invalid leading zero in patch: %r" % version_string)

        major = int(major)
        minor = cls.coerce(minor, partial)
        patch = cls.coerce(patch, partial)

        if prerelease is None:
            if partial and (build is None):
                # No build info, strip here
                return (major, minor, patch, None, None)
            else:
                prerelease = ()
        elif prerelease == '':
            prerelease = ()
        else:
            prerelease = tuple(prerelease.split('.'))
            cls.validate_identifiers(prerelease, allow_leading_zeroes=False)

        if build is None:
            if partial:
                build = None
            else:
                build = ()
        elif build == '':
            build = ()
        else:
            build = tuple(build.split('.'))
            cls.validate_identifiers(build, allow_leading_zeroes=True)

        return (major, minor, patch, prerelease, build)

    def __cmp__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        if self < other:
            return -1
        elif self > other:
            return 1
        elif self == other:
            return 0
        else:
            return NotImplemented

def main():
    version = Version('0.1.1')

    # print(dir(version))
    print(version)

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 7:11 PM
# © 2017 - 2019 DAMGteam. All rights reserved