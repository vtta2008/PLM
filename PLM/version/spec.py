# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import re
from .base import Version


DEFAULT_SYNTAX = 'simple'


class BaseSpec(object):
    """A specification of compatible versions.

    Usage:
    >>> Spec('>=1.0.0', syntax='npm')

    A version matches a specification if it matches any of the clauses of that specification.

    Internally, a Spec is AnyOf(AllOf(Matcher, Matcher, Matcher), AllOf(...),)
    """
    SYNTAXES = {}

    @classmethod
    def register_syntax(cls, subclass):
        syntax = subclass.SYNTAX
        if syntax is None:
            raise ValueError("A Spec needs its SYNTAX field to be set.")
        elif syntax in cls.SYNTAXES:
            raise ValueError(
                "Duplicate syntax for %s: %r, %r"
                % (syntax, cls.SYNTAXES[syntax], subclass)
            )
        cls.SYNTAXES[syntax] = subclass
        return subclass

    def __init__(self, expression):
        super(BaseSpec, self).__init__()
        self.expression = expression
        self.clause = self._parse_to_clause(expression)

    @classmethod
    def parse(cls, expression, syntax=DEFAULT_SYNTAX):
        """Convert a syntax-specific expression into a BaseSpec instance."""
        return cls.SYNTAXES[syntax](expression)

    @classmethod
    def _parse_to_clause(cls, expression):
        """Converts an expression to a clause."""
        raise NotImplementedError()

    def filter(self, versions):
        """Filter an iterable of versions satisfying the Spec."""
        for version in versions:
            if self.match(version):
                yield version

    def match(self, version):
        """Check whether a Version satisfies the Spec."""
        return self.clause.match(version)

    def select(self, versions):
        """Select the best compatible version among an iterable of options."""
        options = list(self.filter(versions))
        if options:
            return max(options)
        return None

    def __contains__(self, version):
        """Whether `version in self`."""
        if isinstance(version, Version):
            return self.match(version)
        return False

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.clause == other.clause

    def __hash__(self):
        return hash(self.clause)

    def __str__(self):
        return self.expression

    def __repr__(self):
        return '<%s: %r>' % (self.__class__.__name__, self.expression)


class Clause(object):

    __slots__ = []

    def match(self, version):
        raise NotImplementedError()

    def __and__(self, other):
        raise NotImplementedError()

    def __or__(self, other):
        raise NotImplementedError()

    def __eq__(self, other):
        raise NotImplementedError()

    def prettyprint(self, indent='\t'):
        """Pretty-print the clause.
        """
        return '\n'.join(self._pretty()).replace('\t', indent)

    def _pretty(self):
        """Actual pretty-printing logic.

        Yields:
            A list of string. Indentation is performed with \t.
        """
        yield repr(self)

    def __ne__(self, other):
        return not self == other

    def simplify(self):
        return self


class AnyOf(Clause):

    __slots__ = ['clauses']

    def __init__(self, *clauses):
        super(AnyOf, self).__init__()
        self.clauses = frozenset(clauses)

    def match(self, version):
        return any(c.match(version) for c in self.clauses)

    def simplify(self):
        subclauses = set()
        for clause in self.clauses:
            simplified = clause.simplify()
            if isinstance(simplified, AnyOf):
                subclauses |= simplified.clauses
            elif simplified == Never():
                continue
            else:
                subclauses.add(simplified)
        if len(subclauses) == 1:
            return subclauses.pop()
        return AnyOf(*subclauses)

    def __hash__(self):
        return hash((AnyOf, self.clauses))

    def __iter__(self):
        return iter(self.clauses)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.clauses == other.clauses

    def __and__(self, other):
        if isinstance(other, AllOf):
            return other & self
        elif isinstance(other, Matcher) or isinstance(other, AnyOf):
            return AllOf(self, other)
        else:
            return NotImplemented

    def __or__(self, other):
        if isinstance(other, AnyOf):
            clauses = list(self.clauses | other.clauses)
        elif isinstance(other, Matcher) or isinstance(other, AllOf):
            clauses = list(self.clauses | set([other]))
        else:
            return NotImplemented
        return AnyOf(*clauses)

    def __repr__(self):
        return 'AnyOf(%s)' % ', '.join(sorted(repr(c) for c in self.clauses))

    def _pretty(self):
        yield 'AnyOF('
        for clause in self.clauses:
            lines = list(clause._pretty())
            for line in lines[:-1]:
                yield '\t' + line
            yield '\t' + lines[-1] + ','
        yield ')'


class AllOf(Clause):

    __slots__ = ['clauses']

    def __init__(self, *clauses):
        super(AllOf, self).__init__()
        self.clauses = frozenset(clauses)

    def match(self, version):
        return all(clause.match(version) for clause in self.clauses)

    def simplify(self):
        subclauses = set()
        for clause in self.clauses:
            simplified = clause.simplify()
            if isinstance(simplified, AllOf):
                subclauses |= simplified.clauses
            elif simplified == Always():
                continue
            else:
                subclauses.add(simplified)
        if len(subclauses) == 1:
            return subclauses.pop()
        return AllOf(*subclauses)

    def __hash__(self):
        return hash((AllOf, self.clauses))

    def __iter__(self):
        return iter(self.clauses)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.clauses == other.clauses

    def __and__(self, other):
        if isinstance(other, Matcher) or isinstance(other, AnyOf):
            clauses = list(self.clauses | set([other]))
        elif isinstance(other, AllOf):
            clauses = list(self.clauses | other.clauses)
        else:
            return NotImplemented
        return AllOf(*clauses)

    def __or__(self, other):
        if isinstance(other, AnyOf):
            return other | self
        elif isinstance(other, Matcher):
            return AnyOf(self, AllOf(other))
        elif isinstance(other, AllOf):
            return AnyOf(self, other)
        else:
            return NotImplemented

    def __repr__(self):
        return 'AllOf(%s)' % ', '.join(sorted(repr(c) for c in self.clauses))

    def _pretty(self):
        yield 'AllOF('
        for clause in self.clauses:
            lines = list(clause._pretty())
            for line in lines[:-1]:
                yield '\t' + line
            yield '\t' + lines[-1] + ','
        yield ')'


class Matcher(Clause):

    __slots__ = []

    def __and__(self, other):
        if isinstance(other, AllOf):
            return other & self
        elif isinstance(other, Matcher) or isinstance(other, AnyOf):
            return AllOf(self, other)
        else:
            return NotImplemented

    def __or__(self, other):
        if isinstance(other, AnyOf):
            return other | self
        elif isinstance(other, Matcher) or isinstance(other, AllOf):
            return AnyOf(self, other)
        else:
            return NotImplemented


class Never(Matcher):

    __slots__ = []

    def match(self, version):
        return False

    def __hash__(self):
        return hash((Never,))

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __and__(self, other):
        return self

    def __or__(self, other):
        return other

    def __repr__(self):
        return 'Never()'


class Always(Matcher):

    __slots__ = []

    def match(self, version):
        return True

    def __hash__(self):
        return hash((Always,))

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __and__(self, other):
        return other

    def __or__(self, other):
        return self

    def __repr__(self):
        return 'Always()'


class Range(Matcher):

    OP_EQ = '=='
    OP_GT = '>'
    OP_GTE = '>='
    OP_LT = '<'
    OP_LTE = '<='
    OP_NEQ = '!='

    # <1.2.3 matches 1.2.3-a1
    PRERELEASE_ALWAYS = 'always'
    # <1.2.3 does not match 1.2.3-a1
    PRERELEASE_NATURAL = 'natural'
    # 1.2.3-a1 is only considered if target == 1.2.3-xxx
    PRERELEASE_SAMEPATCH = 'same-patch'

    # 1.2.3 matches 1.2.3+*
    BUILD_IMPLICIT = 'implicit'
    # 1.2.3 matches only 1.2.3, not 1.2.3+4
    BUILD_STRICT = 'strict'

    __slots__ = ['operator', 'target', 'prerelease_policy', 'build_policy']

    def __init__(self, operator, target, prerelease_policy=PRERELEASE_NATURAL, build_policy=BUILD_IMPLICIT):
        super(Range, self).__init__()
        if target.build and operator not in (self.OP_EQ, self.OP_NEQ):
            raise ValueError(
                "Invalid range %s%s: build numbers have no ordering."
                % (operator, target))
        self.operator = operator
        self.target = target
        self.prerelease_policy = prerelease_policy
        self.build_policy = self.BUILD_STRICT if target.build else build_policy

    def match(self, version):
        if self.build_policy != self.BUILD_STRICT:
            version = version.truncate('prerelease')

        if version.prerelease:
            same_patch = self.target.truncate() == version.truncate()

            if self.prerelease_policy == self.PRERELEASE_SAMEPATCH and not same_patch:
                return False

        if self.operator == self.OP_EQ:
            if self.build_policy == self.BUILD_STRICT:
                return (
                    self.target.truncate('prerelease') == version.truncate('prerelease')
                    and version.build == self.target.build
                )
            return version == self.target
        elif self.operator == self.OP_GT:
            return version > self.target
        elif self.operator == self.OP_GTE:
            return version >= self.target
        elif self.operator == self.OP_LT:
            if (
                version.prerelease
                and self.prerelease_policy == self.PRERELEASE_NATURAL
                and version.truncate() == self.target.truncate()
                and not self.target.prerelease
            ):
                return False
            return version < self.target
        elif self.operator == self.OP_LTE:
            return version <= self.target
        else:
            assert self.operator == self.OP_NEQ
            if self.build_policy == self.BUILD_STRICT:
                return not (
                    self.target.truncate('prerelease') == version.truncate('prerelease')
                    and version.build == self.target.build
                )

            if (
                version.prerelease
                and self.prerelease_policy == self.PRERELEASE_NATURAL
                and version.truncate() == self.target.truncate()
                and not self.target.prerelease
            ):
                return False
            return version != self.target

    def __hash__(self):
        return hash((Range, self.operator, self.target, self.prerelease_policy))

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.operator == other.operator
            and self.target == other.target
            and self.prerelease_policy == other.prerelease_policy
        )

    def __str__(self):
        return '%s%s' % (self.operator, self.target)

    def __repr__(self):
        policy_part = (
            '' if self.prerelease_policy == self.PRERELEASE_NATURAL
            else ', prerelease_policy=%r' % self.prerelease_policy
        ) + (
            '' if self.build_policy == self.BUILD_IMPLICIT
            else ', build_policy=%r' % self.build_policy
        )
        return 'Range(%r, %r%s)' % (
            self.operator,
            self.target,
            policy_part,
        )


@BaseSpec.register_syntax
class SimpleSpec(BaseSpec):

    SYNTAX = 'simple'

    @classmethod
    def _parse_to_clause(cls, expression):
        return cls.Parser.parse(expression)

    class Parser:
        NUMBER = r'\*|0|[1-9][0-9]*'
        NAIVE_SPEC = re.compile(r"""^
            (?P<op><|<=||=|==|>=|>|!=|\^|~|~=)
            (?P<major>{nb})(?:\.(?P<minor>{nb})(?:\.(?P<patch>{nb}))?)?
            (?:-(?P<prerel>[a-z0-9A-Z.-]*))?
            (?:\+(?P<build>[a-z0-9A-Z.-]*))?
            $
            """.format(nb=NUMBER),
            re.VERBOSE,
        )

        @classmethod
        def parse(cls, expression):
            blocks = expression.split(',')
            clause = Always()
            for block in blocks:
                if not cls.NAIVE_SPEC.match(block):
                    raise ValueError("Invalid simple block %r" % block)
                clause &= cls.parse_block(block)

            return clause

        PREFIX_CARET = '^'
        PREFIX_TILDE = '~'
        PREFIX_COMPATIBLE = '~='
        PREFIX_EQ = '=='
        PREFIX_NEQ = '!='
        PREFIX_GT = '>'
        PREFIX_GTE = '>='
        PREFIX_LT = '<'
        PREFIX_LTE = '<='

        PREFIX_ALIASES = {
            '=': PREFIX_EQ,
            '': PREFIX_EQ,
        }

        EMPTY_VALUES = ['*', 'x', 'X', None]

        @classmethod
        def parse_block(cls, expr):
            if not cls.NAIVE_SPEC.match(expr):
                raise ValueError("Invalid simple spec component: %r" % expr)
            prefix, major_t, minor_t, patch_t, prerel, build = cls.NAIVE_SPEC.match(expr).groups()
            prefix = cls.PREFIX_ALIASES.get(prefix, prefix)

            major = None if major_t in cls.EMPTY_VALUES else int(major_t)
            minor = None if minor_t in cls.EMPTY_VALUES else int(minor_t)
            patch = None if patch_t in cls.EMPTY_VALUES else int(patch_t)

            if major is None:  # '*'
                target = Version(major=0, minor=0, patch=0)
                if prefix not in (cls.PREFIX_EQ, cls.PREFIX_GTE):
                    raise ValueError("Invalid simple spec: %r" % expr)
            elif minor is None:
                target = Version(major=major, minor=0, patch=0)
            elif patch is None:
                target = Version(major=major, minor=minor, patch=0)
            else:
                target = Version(
                    major=major,
                    minor=minor,
                    patch=patch,
                    prerelease=prerel.split('.') if prerel else (),
                    build=build.split('.') if build else (),
                )

            if (major is None or minor is None or patch is None) and (prerel or build):
                raise ValueError("Invalid simple spec: %r" % expr)

            if build is not None and prefix not in (cls.PREFIX_EQ, cls.PREFIX_NEQ):
                raise ValueError("Invalid simple spec: %r" % expr)

            if prefix == cls.PREFIX_CARET:
                # Accept anything with the same most-significant digit
                if target.major:
                    high = target.next_major()
                elif target.minor:
                    high = target.next_minor()
                else:
                    high = target.next_patch()
                return Range(Range.OP_GTE, target) & Range(Range.OP_LT, high)

            elif prefix == cls.PREFIX_TILDE:
                assert major is not None
                # Accept any higher patch in the same minor
                # Might go higher if the initial version was a partial
                if minor is None:
                    high = target.next_major()
                else:
                    high = target.next_minor()
                return Range(Range.OP_GTE, target) & Range(Range.OP_LT, high)

            elif prefix == cls.PREFIX_COMPATIBLE:
                assert major is not None
                # ~1 is 1.0.0..2.0.0; ~=2.2 is 2.2.0..3.0.0; ~=1.4.5 is 1.4.5..1.5.0
                if minor is None or patch is None:
                    # We got a partial version
                    high = target.next_major()
                else:
                    high = target.next_minor()
                return Range(Range.OP_GTE, target) & Range(Range.OP_LT, high)

            elif prefix == cls.PREFIX_EQ:
                if major is None:
                    return Range(Range.OP_GTE, target)
                elif minor is None:
                    return Range(Range.OP_GTE, target) & Range(Range.OP_LT, target.next_major())
                elif patch is None:
                    return Range(Range.OP_GTE, target) & Range(Range.OP_LT, target.next_minor())
                elif build == '':
                    return Range(Range.OP_EQ, target, build_policy=Range.BUILD_STRICT)
                else:
                    return Range(Range.OP_EQ, target)

            elif prefix == cls.PREFIX_NEQ:
                assert major is not None
                if minor is None:
                    # !=1.x => <1.0.0 || >=2.0.0
                    return Range(Range.OP_LT, target) | Range(Range.OP_GTE, target.next_major())
                elif patch is None:
                    # !=1.2.x => <1.2.0 || >=1.3.0
                    return Range(Range.OP_LT, target) | Range(Range.OP_GTE, target.next_minor())
                elif prerel == '':
                    # !=1.2.3-
                    return Range(Range.OP_NEQ, target, prerelease_policy=Range.PRERELEASE_ALWAYS)
                elif build == '':
                    # !=1.2.3+ or !=1.2.3-a2+
                    return Range(Range.OP_NEQ, target, build_policy=Range.BUILD_STRICT)
                else:
                    return Range(Range.OP_NEQ, target)

            elif prefix == cls.PREFIX_GT:
                assert major is not None
                if minor is None:
                    # >1.x => >=2.0
                    return Range(Range.OP_GTE, target.next_major())
                elif patch is None:
                    return Range(Range.OP_GTE, target.next_minor())
                else:
                    return Range(Range.OP_GT, target)

            elif prefix == cls.PREFIX_GTE:
                return Range(Range.OP_GTE, target)

            elif prefix == cls.PREFIX_LT:
                assert major is not None
                if prerel == '':
                    # <1.2.3-
                    return Range(Range.OP_LT, target, prerelease_policy=Range.PRERELEASE_ALWAYS)
                return Range(Range.OP_LT, target)

            else:
                assert prefix == cls.PREFIX_LTE
                assert major is not None
                if minor is None:
                    # <=1.x => <2.0
                    return Range(Range.OP_LT, target.next_major())
                elif patch is None:
                    return Range(Range.OP_LT, target.next_minor())
                else:
                    return Range(Range.OP_LTE, target)


@BaseSpec.register_syntax
class NpmSpec(BaseSpec):

    SYNTAX = 'npm'

    @classmethod
    def _parse_to_clause(cls, expression):
        return cls.Parser.parse(expression)

    class Parser:
        JOINER = '||'
        HYPHEN = ' - '

        NUMBER = r'x|X|\*|0|[1-9][0-9]*'
        PART = r'[a-zA-Z0-9.-]*'
        NPM_SPEC_BLOCK = re.compile(r"""
            ^(?:v)?                     # Strip optional initial v
            (?P<op><|<=|>=|>|=|\^|~|)   # Operator, can be empty
            (?P<major>{nb})(?:\.(?P<minor>{nb})(?:\.(?P<patch>{nb}))?)?
            (?:-(?P<prerel>{part}))?    # Optional re-release
            (?:\+(?P<build>{part}))?    # Optional build
            $""".format(nb=NUMBER, part=PART), re.VERBOSE, )

        @classmethod
        def range(cls, operator, target):
            return Range(operator, target, prerelease_policy=Range.PRERELEASE_SAMEPATCH)

        @classmethod
        def parse(cls, expression):
            result = Never()
            groups = expression.split(cls.JOINER)
            for group in groups:
                group = group.strip()
                if not group:
                    group = '>=0.0.0'

                subclauses = []
                if cls.HYPHEN in group:
                    low, high = group.split(cls.HYPHEN, 2)
                    subclauses = cls.parse_simple('>=' + low) + cls.parse_simple('<=' + high)

                else:
                    blocks = group.split(' ')
                    for block in blocks:
                        if not cls.NPM_SPEC_BLOCK.match(block):
                            raise ValueError("Invalid NPM block in %r: %r" % (expression, block))

                        subclauses.extend(cls.parse_simple(block))

                prerelease_clauses = []
                non_prerel_clauses = []
                for clause in subclauses:
                    if clause.target.prerelease:
                        if clause.operator in (Range.OP_GT, Range.OP_GTE):
                            prerelease_clauses.append(Range(
                                operator=Range.OP_LT,
                                target=Version(
                                    major=clause.target.major,
                                    minor=clause.target.minor,
                                    patch=clause.target.patch + 1,
                                ),
                                prerelease_policy=Range.PRERELEASE_ALWAYS,
                            ))
                        elif clause.operator in (Range.OP_LT, Range.OP_LTE):
                            prerelease_clauses.append(Range(
                                operator=Range.OP_GTE,
                                target=Version(
                                    major=clause.target.major,
                                    minor=clause.target.minor,
                                    patch=0,
                                    prerelease=(),
                                ),
                                prerelease_policy=Range.PRERELEASE_ALWAYS,
                            ))
                        prerelease_clauses.append(clause)
                        non_prerel_clauses.append(cls.range(
                            operator=clause.operator,
                            target=clause.target.truncate(),
                        ))
                    else:
                        non_prerel_clauses.append(clause)
                if prerelease_clauses:
                    result |= AllOf(*prerelease_clauses)
                result |= AllOf(*non_prerel_clauses)

            return result

        PREFIX_CARET = '^'
        PREFIX_TILDE = '~'
        PREFIX_EQ = '='
        PREFIX_GT = '>'
        PREFIX_GTE = '>='
        PREFIX_LT = '<'
        PREFIX_LTE = '<='

        PREFIX_ALIASES = {
            '': PREFIX_EQ,
        }

        PREFIX_TO_OPERATOR = {
            PREFIX_EQ: Range.OP_EQ,
            PREFIX_LT: Range.OP_LT,
            PREFIX_LTE: Range.OP_LTE,
            PREFIX_GTE: Range.OP_GTE,
            PREFIX_GT: Range.OP_GT,
        }

        EMPTY_VALUES = ['*', 'x', 'X', None]

        @classmethod
        def parse_simple(cls, simple):
            match = cls.NPM_SPEC_BLOCK.match(simple)

            prefix, major_t, minor_t, patch_t, prerel, build = match.groups()

            prefix = cls.PREFIX_ALIASES.get(prefix, prefix)
            major = None if major_t in cls.EMPTY_VALUES else int(major_t)
            minor = None if minor_t in cls.EMPTY_VALUES else int(minor_t)
            patch = None if patch_t in cls.EMPTY_VALUES else int(patch_t)

            if build is not None and prefix not in [cls.PREFIX_EQ]:
                # Ignore the 'build' part when not comparing to a specific part.
                build = None

            if major is None:  # '*', 'x', 'X'
                target = Version(major=0, minor=0, patch=0)
                if prefix not in [cls.PREFIX_EQ, cls.PREFIX_GTE]:
                    raise ValueError("Invalid expression %r" % simple)
                prefix = cls.PREFIX_GTE
            elif minor is None:
                target = Version(major=major, minor=0, patch=0)
            elif patch is None:
                target = Version(major=major, minor=minor, patch=0)
            else:
                target = Version(
                    major=major,
                    minor=minor,
                    patch=patch,
                    prerelease=prerel.split('.') if prerel else (),
                    build=build.split('.') if build else (),
                )

            if (major is None or minor is None or patch is None) and (prerel or build):
                raise ValueError("Invalid NPM spec: %r" % simple)

            if prefix == cls.PREFIX_CARET:
                if target.major:  # ^1.2.4 => >=1.2.4 <2.0.0 ; ^1.x => >=1.0.0 <2.0.0
                    high = target.truncate().next_major()
                elif target.minor:  # ^0.1.2 => >=0.1.2 <0.2.0
                    high = target.truncate().next_minor()
                elif minor is None:  # ^0.x => >=0.0.0 <1.0.0
                    high = target.truncate().next_major()
                elif patch is None:  # ^0.2.x => >=0.2.0 <0.3.0
                    high = target.truncate().next_minor()
                else:  # ^0.0.1 => >=0.0.1 <0.0.2
                    high = target.truncate().next_patch()
                return [cls.range(Range.OP_GTE, target), cls.range(Range.OP_LT, high)]

            elif prefix == cls.PREFIX_TILDE:
                assert major is not None
                if minor is None:  # ~1.x => >=1.0.0 <2.0.0
                    high = target.next_major()
                else:  # ~1.2.x => >=1.2.0 <1.3.0; ~1.2.3 => >=1.2.3 <1.3.0
                    high = target.next_minor()
                return [cls.range(Range.OP_GTE, target), cls.range(Range.OP_LT, high)]

            elif prefix == cls.PREFIX_EQ:
                if major is None:
                    return [cls.range(Range.OP_GTE, target)]
                elif minor is None:
                    return [cls.range(Range.OP_GTE, target), cls.range(Range.OP_LT, target.next_major())]
                elif patch is None:
                    return [cls.range(Range.OP_GTE, target), cls.range(Range.OP_LT, target.next_minor())]
                else:
                    return [cls.range(Range.OP_EQ, target)]

            elif prefix == cls.PREFIX_GT:
                assert major is not None
                if minor is None:  # >1.x
                    return [cls.range(Range.OP_GTE, target.next_major())]
                elif patch is None:  # >1.2.x => >=1.3.0
                    return [cls.range(Range.OP_GTE, target.next_minor())]
                else:
                    return [cls.range(Range.OP_GT, target)]

            elif prefix == cls.PREFIX_GTE:
                return [cls.range(Range.OP_GTE, target)]

            elif prefix == cls.PREFIX_LT:
                assert major is not None
                return [cls.range(Range.OP_LT, target)]

            else:
                assert prefix == cls.PREFIX_LTE
                assert major is not None
                if minor is None:  # <=1.x => <2.0.0
                    return [cls.range(Range.OP_LT, target.next_major())]
                elif patch is None:  # <=1.2.x => <1.3.0
                    return [cls.range(Range.OP_LT, target.next_minor())]
                else:
                    return [cls.range(Range.OP_LTE, target)]

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
