# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from typing import Dict, Optional, Text, Mapping, MutableMapping
from abc import ABCMeta, abstractmethod as abstract_method
from pkg_resources import iter_entry_points
from collections import OrderedDict, defaultdict
from functools import cmp_to_key
from six import PY2, iteritems, with_metaclass, iterkeys
from inspect import isclass as is_class
from inspect import isabstract as is_abstract

__all__ = [
    'EntryPointClassRegistry',
    'AutoRegister',
    'BaseRegistry',
    'MutableRegistry',
    'ClassRegistry',
    'ClassRegistryInstanceCache',
    'RegistryPatcher'
]


def AutoRegister(registry, base_type=ABCMeta):
    # type: (MutableRegistry, type) -> type

    if not registry.attr_name:
        raise ValueError(
            'Missing `attr_name` in {registry}.'.format(registry=registry),
        )

    class _metaclass(base_type):
        def __init__(self, what, bases=None, attrs=None):
            super(_metaclass, self).__init__(what, bases, attrs)

            if not is_abstract(self):
                registry.register(self)

    return _metaclass

class RegistryKeyError(KeyError):
    pass

class BaseRegistry(with_metaclass(ABCMeta, Mapping)):
    def __contains__(self, key):
        try:
            self.get_class(key)
        except RegistryKeyError:
            return False
        else:
            return True

    def __dir__(self):
        return list(self.keys())

    def __getitem__(self, key):
        return self.get(key)

    def __iter__(self):
        # type: () -> Generator[Hashable]
        return self.keys()

    @abstract_method
    def __len__(self):
        # type: () -> int
        raise NotImplementedError(
            'Not implemented in {cls}.'.format(cls=type(self).__name__),
        )

    def __missing__(self, key):
        raise RegistryKeyError(key)

    @abstract_method
    def get_class(self, key):
        raise NotImplementedError(
            'Not implemented in {cls}.'.format(cls=type(self).__name__),
        )

    def get(self, key, *args, **kwargs):
        return self.create_instance(self.get_class(key), *args, **kwargs)

    @staticmethod
    def gen_lookup_key(key):
        # type: (Any) -> Hashable
        return key

    @staticmethod
    def create_instance(class_, *args, **kwargs):
        # type: (type, *Any, **Any) -> Any
        return class_(*args, **kwargs)

    @abstract_method
    def items(self):
        # type: () -> Generator[Tuple[Hashable, type]]
        raise NotImplementedError(
            'Not implemented in {cls}.'.format(cls=type(self).__name__),
        )

    def keys(self):
        # type: () -> Generator[Hashable]
        for item in self.items():
            yield item[0]

    def values(self):
        # type: () -> Generator[type]
        for item in self.items():
            yield item[1]
    if PY2:
        def iteritems(self):
            return self.items()

        def iterkeys(self):
            return self.keys()

        def itervalues(self):
            return self.values()

class MutableRegistry(with_metaclass(ABCMeta, BaseRegistry, MutableMapping)):
    def __init__(self, attr_name=None):
        # type: (Optional[Text]) -> None
        super(MutableRegistry, self).__init__()
        self.attr_name = attr_name

    def __delitem__(self, key):
        # type: (Hashable) -> None
        self._unregister(key)

    def __repr__(self):
        return '{type}({attr_name!r})'.format(
            attr_name   = self.attr_name,
            type        = type(self).__name__,
        )

    def __setitem__(self, key, class_):
        # type: (Text, type) -> None
        self._register(key, class_)

    def register(self, key):

        if is_class(key):
            if self.attr_name:
                self._register(getattr(key, self.attr_name), key)
                return key
            else:
                raise ValueError('Registry key is required.')

        def _decorator(cls):
            self._register(key, cls)
            return cls
        return _decorator

    def unregister(self, key):
        # type: (Any) -> type
        return self._unregister(self.gen_lookup_key(key))

    @abstract_method
    def _register(self, key, class_):
        # type: (Hashable, type) -> None
        raise NotImplementedError(
            'Not implemented in {cls}.'.format(cls=type(self).__name__),
        )

    @abstract_method
    def _unregister(self, key):
        # type: (Hashable) -> type
        raise NotImplementedError('Not implemented in {cls}.'.format(cls=type(self).__name__),)

class ClassRegistry(MutableRegistry):
    def __init__(self, attr_name=None, unique=False):
        # type: (Optional[Text], bool) -> None
        super(ClassRegistry, self).__init__(attr_name)
        self.unique = unique
        self._registry = OrderedDict()

    def __len__(self):
        # type: () -> int
        return len(self._registry)

    def __repr__(self):
        return '{type}(attr_name={attr_name!r}, unique={unique!r})'.format(
            attr_name   = self.attr_name,
            type        = type(self).__name__,
            unique      = self.unique,
        )

    def get_class(self, key):
        lookup_key = self.gen_lookup_key(key)
        try:
            return self._registry[lookup_key]
        except KeyError:
            return self.__missing__(lookup_key)

    def items(self):
        # type: () -> Iterator[Tuple[Hashable, type]]
        return iteritems(self._registry)

    def _register(self, key, class_):
        # type: (Hashable, type) -> None
        if key in ['', None]:
            raise ValueError('Attempting to register class {cls} with empty registry key {key!r}.'.format(cls = class_.__name__, key = key,  ),  )

        if self.unique and (key in self._registry):
            raise RegistryKeyError('{cls} with key {key!r} is already registered.'.format(cls = class_.__name__, key = key,),)

        self._registry[key] = class_

    def _unregister(self, key):
        # type: (Hashable) -> type
        return (self._registry.pop(key) if key in self._registry else self.__missing__(key))

class SortedClassRegistry(ClassRegistry):
    def __init__(
            self,
            sort_key,                   # type: Union[Text, Callable[[Tuple[Hashable, type], Tuple[Hashable, type]], int]]
            attr_name       = None,     # type: Optional[Text]
            unique          = False,    # type: bool
            reverse         = False,    # type: bool
    ):

        super(SortedClassRegistry, self).__init__(attr_name, unique)

        self._sort_key = (
            sort_key
                if callable(sort_key)
                else self.create_sorter(sort_key)
        )

        self.reverse = reverse

    def items(self):
        # type: () -> Iterator[Tuple[Hashable, type]]
        return sorted(
            iteritems(self._registry),
                key     = self._sort_key,
                reverse = self.reverse,
        )

    @staticmethod
    def create_sorter(sort_key):
        def sorter(a, b):
            # type: (Tuple[Hashable, type], Tuple[Hashable, type]) -> int
            a_attr = getattr(a[1], sort_key)
            b_attr = getattr(b[1], sort_key)

            return (a_attr > b_attr) - (a_attr < b_attr)

        return cmp_to_key(sorter)

class EntryPointClassRegistry(BaseRegistry):

    def __init__(self, group, attr_name=None):
        # type: (Text, Optional[Text]) -> None
        super(EntryPointClassRegistry, self).__init__()

        self.attr_name  = attr_name
        self.group      = group

        self._cache = None # type: Optional[Dict[Text, type]]
        if self.attr_name:
            self._get_cache()

    def __len__(self):
        return len(self._get_cache())

    def __repr__(self):
        return '{type}(group={group!r})'.format(
            group   = self.group,
            type    = type(self).__name__,
        )

    def get(self, key, *args, **kwargs):
        instance =\
            super(EntryPointClassRegistry, self).get(key, *args, **kwargs)
        if self.attr_name:
            setattr(instance, self.attr_name, key)
        return instance

    def get_class(self, key):
        try:
            cls = self._get_cache()[key]
        except KeyError:
            cls = self.__missing__(key)
        return cls

    def items(self):
        return iteritems(self._get_cache())

    def refresh(self):
        self._cache = None

    def _get_cache(self):
        # type: () -> Dict[Text, type]
        if self._cache is None:
            self._cache = {}
            for e in iter_entry_points(self.group):
                cls = e.load()
                if self.attr_name and isinstance(cls, type):
                    setattr(cls, self.attr_name, e.name)
                self._cache[e.name] = cls
        return self._cache

class ClassRegistryInstanceCache(object):

    def __init__(self, class_registry, *args, **kwargs):
        # type: (ClassRegistry, *Any, **Any) -> None

        super(ClassRegistryInstanceCache, self).__init__()

        self._registry  = class_registry
        self._cache     = {}

        self._key_map = defaultdict(list) # type: Dict[Hashable, list]

        self._template_args     = args
        self._template_kwargs   = kwargs

    def __getitem__(self, key):

        instance_key = self.get_instance_key(key)

        if instance_key not in self._cache:
            class_key = self.get_class_key(key)

            self._key_map[class_key].append(instance_key)

            self._cache[instance_key] =\
                self._registry.get(
                    class_key,
                    *self._template_args,
                    **self._template_kwargs
                )

        return self._cache[instance_key]

    def __iter__(self):
        # type: () -> Generator[Any]
        for lookup_key in iterkeys(self._registry):
            for cache_key in self._key_map[lookup_key]:
                yield self._cache[cache_key]

    def warm_cache(self):
        for key in iterkeys(self._registry):
            self.__getitem__(key)

    def get_instance_key(self, key):
        # type: (Any) -> Hashable
        return self.get_class_key(key)

    def get_class_key(self, key):
        # type: (Any) -> Hashable
        return self._registry.gen_lookup_key(key)

class RegistryPatcher(object):

    class DoesNotExist(object):
        pass

    def __init__(self, registry, *args, **kwargs):
        # type: (MutableRegistry, *Any, **Any) -> None

        super(RegistryPatcher, self).__init__()

        for class_ in args:
            kwargs[getattr(class_, registry.attr_name)] = class_

        self.target = registry

        self._new_values  = kwargs
        self._prev_values = {}

    def __enter__(self):
        self.apply()


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.restore()

    def apply(self):
        self._prev_values = {
            key: self._get_value(key, self.DoesNotExist)
                for key in self._new_values
        }


        for key, value in iteritems(self._new_values):
            self._del_value(key)
            if value is not self.DoesNotExist:
                self._set_value(key, value)

    def restore(self):
        for key, value in iteritems(self._prev_values):
            self._del_value(key)

            if value is not self.DoesNotExist:
                self._set_value(key, value)

    def _get_value(self, key, default=None):
        try:
            return self.target.get_class(key)
        except RegistryKeyError:
            return default

    def _set_value(self, key, value):
        self.target.register(key)(value)

    def _del_value(self, key):
        try:
            self.target.unregister(key)
        except RegistryKeyError:
            pass