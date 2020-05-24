# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, textwrap

from collections.abc import Hashable
from humanfriendly import coerce_boolean
from humanfriendly.tables import format_rst_table
from humanfriendly.text import compact, concatenate, format, pluralize


basestring = str

# PLM
from PLM.loggers import Loggers


SPHINX_ACTIVE = 'sphinx' in sys.modules

USAGE_NOTES_VARIABLE = 'PROPERTY_MANAGER_USAGE_NOTES'

USAGE_NOTES_ENABLED = (coerce_boolean(os.environ[USAGE_NOTES_VARIABLE]) if USAGE_NOTES_VARIABLE in os.environ else SPHINX_ACTIVE)

NOTHING = object()

CUSTOM_PROPERTY_NOTE = compact(""" The :attr:`{name}` property is a :class:`~{type}`. """)

DYNAMIC_PROPERTY_NOTE = compact(""" The :attr:`{name}` property is a :class:`~{type}`. """)

ENVIRONMENT_PROPERTY_NOTE = compact(""" If the environment variable ``${variable}`` is set it overrides the computed 
                                        value of this property. """)

REQUIRED_PROPERTY_NOTE = compact(""" You are required to provide a value for this property by calling the constructor of 
                                    the class that defines the property with a keyword argument named `{name}` (unless 
                                    a custom constructor is defined, in this case please refer to the documentation of 
                                    that constructor). """)

KEY_PROPERTY_NOTE = compact(""" Once this property has been assigned a value you are not allowed to assign a new value 
                                to the property. """)

WRITABLE_PROPERTY_NOTE = compact(""" You can change the value of this property using normal attribute assignment syntax. """)

CACHED_PROPERTY_NOTE = compact(""" This property's value is computed once (the first time it is accessed) and the result 
                                    is cached.""")

RESETTABLE_CACHED_PROPERTY_NOTE = compact(""" To clear the cached value you can use :keyword:`del` or :func:`delattr()`. """)

RESETTABLE_WRITABLE_PROPERTY_NOTE = compact(""" To reset it to its default (computed) value you can use :keyword:`del` or :func:`delattr()`. """)


logger = Loggers(__name__)


def set_property(obj, name, value):
    logger.spam("Setting value of %s property to %r ..", format_property(obj, name), value)
    obj.__dict__[name] = value


def clear_property(obj, name):
    logger.spam("Clearing value of %s property ..", format_property(obj, name))
    obj.__dict__.pop(name, None)


def format_property(obj, name):
    return "%s.%s" % (obj.__class__.__name__, name)



class PropertyManager(object):

    def __init__(self, **kw):
        self.set_properties(**kw)
        missing_properties = self.missing_properties
        if missing_properties:
            msg = "missing %s" % pluralize(len(missing_properties), "required argument")
            raise TypeError("%s (%s)" % (msg, concatenate(missing_properties)))

    def set_properties(self, **kw):
        for name, value in kw.items():
            if self.have_property(name):
                setattr(self, name, value)
            else:
                msg = "got an unexpected keyword argument %r"
                raise TypeError(msg % name)

    @property
    def key_properties(self):
        return self.find_properties(key=True)

    @property
    def key_values(self):
        return tuple((name, getattr(self, name)) for name in self.key_properties)

    @property
    def missing_properties(self):
        names = sorted(set(self.required_properties) | set(self.key_properties))
        return [n for n in names if getattr(self, n, None) is None]

    @property
    def repr_properties(self):
        return self.key_properties or [name for name in self.find_properties(repr=True) if not hasattr(PropertyManager, name)]

    @property
    def required_properties(self):
        return self.find_properties(required=True)

    def find_properties(self, **options):
        return [n for n in dir(self) if self.have_property(n, **options)]

    def have_property(self, name, **options):
        property_type = getattr(self.__class__, name, None)

        if isinstance(property_type, property):
            if options:
                return all(getattr(property_type, n, None) == v or
                           n == 'repr' and v is True and getattr(property_type, n, None) is not False
                           for n, v in options.items())
            else:
                return True
        else:
            return False

    def clear_cached_properties(self):

        for name in self.find_properties(cached=True, resettable=True):
            delattr(self, name)

    def render_properties(self, *names):

        fields = []
        for name in names:
            value = getattr(self, name, None)
            if value is not None or name in self.key_properties:
                fields.append("%s=%r" % (name, value))
        return "%s(%s)" % (self.__class__.__name__, ", ".join(fields))

    def __eq__(self, other):

        our_key = self.key_values
        return (our_key == other.key_values
                if our_key and isinstance(other, PropertyManager)
                else NotImplemented)

    def __ne__(self, other):

        our_key = self.key_values
        return (our_key != other.key_values
                if our_key and isinstance(other, PropertyManager)
                else NotImplemented)

    def __lt__(self, other):

        our_key = self.key_values
        return (our_key < other.key_values
                if our_key and isinstance(other, PropertyManager)
                else NotImplemented)

    def __le__(self, other):

        our_key = self.key_values
        return (our_key <= other.key_values
                if our_key and isinstance(other, PropertyManager)
                else NotImplemented)

    def __gt__(self, other):

        our_key = self.key_values
        return (our_key > other.key_values
                if our_key and isinstance(other, PropertyManager)
                else NotImplemented)

    def __ge__(self, other):

        our_key = self.key_values
        return (our_key >= other.key_values
                if our_key and isinstance(other, PropertyManager)
                else NotImplemented)

    def __hash__(self):
        return hash(PropertyManager) ^ hash(self.key_values)


    def __repr__(self):
        return self.render_properties(*self.repr_properties)



class DamgProperty(property):

    key                                 = "DamgProperty"


    cached                              = False
    dynamic                             = False
    environment_variable                = None
    repr                                = True
    required                            = False
    resettable                          = False
    usage_notes                         = True
    writable                            = False

    def __new__(cls, *args, **options):

        if options:
            name                        = args[0] if args else 'DamgProperty'
            options['dynamic']          = True
            return type(name, (cls,), options)
        else:
            return super(DamgProperty, cls).__new__(cls, *args)

    def __init__(self, *args, **kw):
        super(DamgProperty, self).__init__(*args, **kw)

        self.ensure_callable('fget')

        for name in 'fset', 'fdel':
            if getattr(self, name) is not None:
                self.ensure_callable(name)

        for name in '__doc__', '__module__', '__name__':
            value                         = getattr(self.fget, name, None)
            if value is not None:
                setattr(self, name, value)

        if USAGE_NOTES_ENABLED:
            self.inject_usage_notes()

    def ensure_callable(self, role):

        value                               = getattr(self, role)
        if not callable(value):
            msg                             = "Invalid '%s' value! (expected callable, got %r instead)"
            raise ValueError(msg % (role, value))

    def inject_usage_notes(self):

        if self.usage_notes and self.__doc__ and isinstance(self.__doc__, basestring):

            notes                           = self.compose_usage_notes()

            if notes:
                self.__doc__                = "\n\n".join([textwrap.dedent(self.__doc__), ".. note:: {0}".
                                                          format(" ".join(notes)), ])

    def compose_usage_notes(self):

        template                            = DYNAMIC_PROPERTY_NOTE if self.dynamic else CUSTOM_PROPERTY_NOTE
        cls                                 = DamgProperty if self.dynamic else self.__class__
        dotted_path                         = "{0}.{1}".format(cls.__module__, cls.__name__)
        notes                               = [format(template, name=self.__name__, type=dotted_path)]

        if self.environment_variable:
            notes.append(format(ENVIRONMENT_PROPERTY_NOTE, variable=self.environment_variable))

        if self.required:
            notes.append(format(REQUIRED_PROPERTY_NOTE, name=self.__name__))

        if self.key:
            notes.append(KEY_PROPERTY_NOTE)

        if self.writable:
            notes.append(WRITABLE_PROPERTY_NOTE)

        if self.cached:
            notes.append(CACHED_PROPERTY_NOTE)

        if self.resettable:
            if self.cached:
                notes.append(RESETTABLE_CACHED_PROPERTY_NOTE)
            else:
                notes.append(RESETTABLE_WRITABLE_PROPERTY_NOTE)

        return notes

    def __get__(self, obj, type=None):

        if obj is None:
            return self
        else:
            dotted_name = format_property(obj, self.__name__)
            if self.key or self.writable or self.cached:

                value = obj.__dict__.get(self.__name__, NOTHING)
                if value is not NOTHING:
                    logger.spam("{0} reporting assigned or cached value ({1}) ..".format(dotted_name, value))
                    return value

            if self.environment_variable:
                value = os.environ.get(self.environment_variable, NOTHING)
                if value is not NOTHING:
                    logger.spam("{0} reporting value from environment variable ({1}) ..".format(dotted_name, value))
                    return value

            value = super(DamgProperty, self).__get__(obj, type)

            logger.spam("%s reporting computed value (%r) ..", dotted_name, value)

            if self.cached:
                logger.spam("{0} caching computed value ..".format(format(dotted_name)))
                set_property(obj, self.__name__, value)

            return value

    def __set__(self, obj, value):

        dotted_name = format_property(obj, self.__name__)

        try:
            logger.spam("{0} calling setter with value {1} ..".format(dotted_name, value))
            super(DamgProperty, self).__set__(obj, value)

        except AttributeError:
            logger.spam("{0} setter raised attribute error, falling back.".format(dotted_name))
            if self.writable:
                logger.spam("{0} overriding computed value to {1} ..".format(dotted_name, value))
                set_property(obj, self.__name__, value)
            else:
                if self.key and obj.__dict__.get(self.__name__, None) is None:
                    if not isinstance(value, Hashable):
                        raise ValueError("Invalid value for key property '{0}'! (expected hashable object, "
                                         "got %r instead)".format(self.__name__, value))

                    logger.spam("{0} setting initial value to {1}  ..".format(dotted_name, value))
                    set_property(obj, self.__name__, value)
                else:
                    raise AttributeError("{0} object attribute {1} is read-only".format(obj.__class__.__name__, self.__name__))

    def __delete__(self, obj):

        dotted_name                         = format_property(obj, self.__name__)

        try:
            logger.spam("{0} calling deleter ..".format(dotted_name))
            super(DamgProperty, self).__delete__(obj)
        except AttributeError:
            logger.spam("{0} deleter raised attribute error, falling back.".format(dotted_name))

            if self.resettable:
                logger.spam("{0} clearing assigned or computed value ..".format(dotted_name))
                clear_property(obj, self.__name__)
            else:
                raise AttributeError("{0} object attribute {1} is read-only".format(obj.__class__.__name__, self.__name__))


class writable_property(DamgProperty):
    writable = True


class required_property(writable_property):
    required = True


class mutable_property(writable_property):
    resettable = True


class lazy_property(DamgProperty):
    cached = True


class cached_property(lazy_property):
    resettable = True



def append_property_docs(app, what, name, obj, options, lines):

    if is_suitable_type(obj):
        paragraphs                              = []
        details                                 = TypeInspector(type=obj)
        paragraphs.append(format("Here's an overview of the :class:`%s` class:", obj.__name__))

        data = [(format("%s:", label.replace(' ', u'\u00A0')), text) for label, text in details.overview if text]
        paragraphs.append(format_rst_table(data))
        # Append any hints after the overview.
        hints = (details.required_hint, details.initializer_hint)
        if any(hints):
            paragraphs.append(' '.join(h for h in hints if h))
        # Insert padding between the regular docstring and generated content.
        if lines:
            lines.append('')
        lines.extend('\n\n'.join(paragraphs).splitlines())


def is_suitable_type(obj):
    try:
        return issubclass(obj, PropertyManager)
    except Exception:
        return False


class TypeInspector(PropertyManager):

    """Introspection of :class:`.PropertyManager` subclasses."""

    @lazy_property
    def custom_properties(self):
        """A list of tuples with the names and values of custom properties."""
        return [(n, v) for n, v in self.properties if isinstance(v, DamgProperty)]

    @lazy_property
    def initializer_hint(self):
        """A hint that properties can be set using keyword arguments to the initializer (a string or :data:`None`)."""
        names = sorted(
            name for name, value in self.custom_properties
            if value.key or value.required or value.writable
        )
        if names:
            return compact(
                """
                You can set the {values} of the {names} {properties}
                by passing {arguments} to the class initializer.
                """,
                names=self.format_properties(names),
                values=("value" if len(names) == 1 else "values"),
                properties=("property" if len(names) == 1 else "properties"),
                arguments=("a keyword argument" if len(names) == 1 else "keyword arguments"),
            )

    @lazy_property
    def members(self):
        """An iterable of tuples with the names and values of the non-inherited members of :class:`type`."""
        return list(self.type.__dict__.items())

    @lazy_property
    def methods(self):
        """An iterable of method names of :class:`type`."""
        return sorted(n for n, v in self.members if isinstance(v, types.FunctionType))

    @lazy_property
    def overview(self):
        """Render an overview with related members grouped together."""
        return (
            ("Superclass" if len(self.type.__bases__) == 1 else "Superclasses",
             concatenate(format(":class:`~%s.%s`", b.__module__, b.__name__) for b in self.type.__bases__)),
            ("Special methods", self.format_methods(self.special_methods)),
            ("Public methods", self.format_methods(self.public_methods)),
            ("Properties", self.format_properties(n for n, v in self.properties)),
        )

    @lazy_property
    def properties(self):
        """An iterable of tuples with property names (strings) and values (:class:`property` objects)."""
        return [(n, v) for n, v in self.members if isinstance(v, property)]

    @lazy_property
    def public_methods(self):
        """An iterable of strings with the names of public methods (that don't start with an underscore)."""
        return sorted(n for n in self.methods if not n.startswith('_'))

    @lazy_property
    def required_hint(self):
        """A hint about required properties (a string or :data:`None`)."""
        names = sorted(name for name, value in self.custom_properties if value.required)
        if names:
            return compact(
                """
                When you initialize a :class:`{type}` object you are required
                to provide {values} for the {required} {properties}.
                """,
                type=self.type.__name__,
                required=self.format_properties(names),
                values=("a value" if len(names) == 1 else "values"),
                properties=("property" if len(names) == 1 else "properties"),
            )

    @lazy_property
    def special_methods(self):
        """An iterable of strings with the names of special methods (surrounded in double underscores)."""
        methods = sorted(name for name in self.methods if name.startswith('__') and name.endswith('__'))
        if '__init__' in methods:
            methods.remove('__init__')
            methods.insert(0, '__init__')
        return methods

    @required_property
    def type(self):
        """A subclass of :class:`.PropertyManager`."""

    def format_methods(self, names):
        """Format a list of method names as reStructuredText."""
        return concatenate(format(":func:`%s()`", n) for n in sorted(names))

    def format_properties(self, names):
        """Format a list of property names as reStructuredText."""
        return concatenate(format(":attr:`%s`", n) for n in sorted(names))



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved