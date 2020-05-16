
CLASS OBJECT ELEMENTS
#####################

ATTRIBUTE
---------
.. list-table::
    :widths: 100 1000 100
    :header-rows: 1

    * - Name
      - Meaning
      - Ability

    * - __doc__
      - The function’s documentation string, or None if unavailable; not inherited by subclasses.
      - Writable

    * - __name__
      - The function’s name.
      - Writable

    * - __qualname__
      - the entire dotted path to the module, including any parent packages.
      - Writable

    * - __module__
      - The name of the module the function was defined in, or None if unavailable.
      - Writable

    * - __defaults__
      - A tuple containing default argument values for those arguments that have defaults, or None if no arguments have a default value.
      - Writable

    * - __code__
      - The code object representing the compiled function body.
      - Writable

    * - __globals__
      - A reference to the dictionary that holds the function’s global variables — the global namespace of the module in which the function was defined.
      - Read-only

    * - __dict__
      - The namespace supporting arbitrary function attributes.
      - Writable

    * - __closure__
      - None or a tuple of cells that contain bindings for the function’s free variables.
      - Read-only

    * - __annotations__
      - A dict containing annotations of parameters. The keys of the dict are the parameter names, and 'return' for the return annotation, if provided.
      - Writable.

    * - __kwdefaults__
      - A dict containing defaults for keyword-only parameters.
      - Writable.

BASIC METHOD
------------


A class can implement certain operations that are invoked by special syntax (such as arithmetic operations or
subscripting and slicing) by defining methods with special names. This is Python’s approach to operator overloading,
allowing classes to define their own behavior with respect to language operators. For instance, if a class defines a
method named __getitem__(), and x is an instance of this class, then x[i] is roughly equivalent to type(x).__getitem__(x, i).
Except where mentioned, attempts to execute an operation raise an exception when no appropriate method is defined (typically
AttributeError or TypeError).

Setting a special method to None indicates that the corresponding operation is not available. For example, if a class
sets __iter__() to None, the class is not iterable, so calling iter() on its instances will raise a TypeError (without
falling back to __getitem__()). 2

When implementing a class that emulates any built-in type, it is important that the emulation only be implemented to
the degree that it makes sense for the object being modelled. For example, some sequences may work well with retrieval
of individual elements, but extracting a slice may not make sense.


.. list-table::
    :widths: 100 1000
    :header-rows: 1

    * - Name
      - Description

    * - __new__(cls[, ...])
      - Called to create a new instance of class cls. __new__() is a static method (special-cased so you need not
        declare it as such) that takes the class of which an instance was requested as its first argument. The remaining
        arguments are those passed to the object constructor expression (the call to the class). The return value
        of __new__() should be the new object instance (usually an instance of cls).

        Typical implementations create a new instance of the class by invoking the superclass’s __new__() method using
        super().__new__(cls[, ...]) with appropriate arguments and then modifying the newly-created instance as necessary
        before returning it.

        If __new__() is invoked during object construction and it returns an instance or subclass of cls, then the new
        instance’s __init__() method will be invoked like __init__(self[, ...]), where self is the new instance and the
        remaining arguments are the same as were passed to the object constructor.

        If __new__() does not return an instance of cls, then the new instance’s __init__() method will not be invoked.

        __new__() is intended mainly to allow subclasses of immutable types (like int, str, or tuple) to customize
        instance creation. It is also commonly overridden in custom metaclasses in order to customize class creation.

    * - __init__(self[, ...])
      - Called after the instance has been created (by __new__()), but before it is returned to the caller. The
        arguments are those passed to the class constructor expression. If a base class has an __init__() method,
        the derived class’s __init__() method, if any, must explicitly call it to ensure proper initialization of the
        base class part of the instance; for example: super().__init__([args...]).

        Because __new__() and __init__() work together in constructing objects (__new__() to create it, and __init__()
        to customize it), no non-None value may be returned by __init__(); doing so will cause a TypeError to be raised
        at runtime.

    * - __del__(self)
      - Called when the instance is about to be destroyed. This is also called a finalizer or (improperly) a destructor.
        If a base class has a __del__() method, the derived class’s __del__() method, if any, must explicitly call it
        to ensure proper deletion of the base class part of the instance.

        It is possible (though not recommended!) for the __del__() method to postpone destruction of the instance by
        creating a new reference to it. This is called object resurrection. It is implementation-dependent
        whether __del__() is called a second time when a resurrected object is about to be destroyed; the current
        CPython implementation only calls it once.

        It is not guaranteed that __del__() methods are called for objects that still exist when the interpreter exits.

    * - __repr__(self)
      - Called by the repr() built-in function to compute the “official” string representation of an object. If at all
        possible, this should look like a valid Python expression that could be used to recreate an object with the same
        value (given an appropriate environment). If this is not possible, a string of the form <...some useful
        description...> should be returned. The return value must be a string object. If a class defines __repr__()
        but not __str__(), then __repr__() is also used when an “informal” string representation of instances of that
        class is required.

        This is typically used for debugging, so it is important that the representation is information-rich and
        unambiguous.

    * - __str__(self)
      - Called by str(object) and the built-in functions format() and print() to compute the “informal” or nicely
        printable string representation of an object. The return value must be a string object.

        This method differs from object.__repr__() in that there is no expectation that __str__() return a valid Python
        expression: a more convenient or concise representation can be used.

        The default implementation defined by the built-in type object calls object.__repr__().

    * - __bytes__(self)
      - Called by bytes to compute a byte-string representation of an object. This should return a bytes object.

    * - __format__(self, format_spec)
      - Called by the format() built-in function, and by extension, evaluation of formatted string literals and the
        str.format() method, to produce a “formatted” string representation of an object. The format_spec argument is
        a string that contains a description of the formatting options desired. The interpretation of the format_spec
        argument is up to the type implementing __format__(), however most classes will either delegate formatting to
        one of the built-in types, or use a similar formatting option syntax.

        See Format Specification Mini-Language for a description of the standard formatting syntax.

        The return value must be a string object.

        Changed in version 3.7: object.__format__(x, '') is now equivalent to str(x) rather than format(str(self), '').


These are the so-called “rich comparison” methods. The correspondence between operator symbols and method names is as
follows: x<y calls x.__lt__(y), x<=y calls x.__le__(y), x==y calls x.__eq__(y), x!=y calls x.__ne__(y), x>y calls
x.__gt__(y), and x>=y calls x.__ge__(y).

A rich comparison method may return the singleton NotImplemented if it does not implement the operation for a given pair
of arguments. By convention, False and True are returned for a successful comparison. However, these methods can return
any value, so if the comparison operator is used in a Boolean context (e.g., in the condition of an if statement),
Python will call bool() on the value to determine if the result is true or false.

By default, __ne__() delegates to __eq__() and inverts the result unless it is NotImplemented. There are no other
implied relationships among the comparison operators, for example, the truth of (x<y or x==y) does not imply x<=y.
To automatically generate ordering operations from a single root operation, see functools.total_ordering().

See the paragraph on __hash__() for some important notes on creating hashable objects which support custom comparison
operations and are usable as dictionary keys.

There are no swapped-argument versions of these methods (to be used when the left argument does not support the operation
but the right argument does); rather, __lt__() and __gt__() are each other’s reflection, __le__() and __ge__() are each
other’s reflection, and __eq__() and __ne__() are their own reflection. If the operands are of different types, and right
operand’s type is a direct or indirect subclass of the left operand’s type, the reflected method of the right operand has
priority, otherwise the left operand’s method has priority. Virtual subclassing is not considered.


.. list-table:: RICH COMPARISON
    :widths: 100 1000
    :header-rows: 1

    * - Name
      - Description

    * - __lt__(self, other)
      -

    * - __le__(self, other)
      -

    * - __eq__(self, other)
      -

    * - __ne__(self, other)
      -

    * - __gt__(self, other)
      -

    * - __ge__(self, other)
      -


DESCRIPTOR
----------

.. list-table::
    :widths: 100 1000
    :header-rows: 1

    * - Name
      - Description

    * - __get__(self, instance, owner=None)
      - Called to get the attribute of the owner class (class attribute access) or of an instance of that class
        (instance attribute access). The optional owner argument is the owner class, while instance is the instance
        that the attribute was accessed through, or None when the attribute is accessed through the owner.

    * - __set__(self, instance, value)
      - Called to set the attribute on an instance instance of the owner class to a new value, value.

    * - __delete__(self, instance)
      - Called to delete the attribute on an instance instance of the owner class.

    * - __call__(args)
      - Called when the instance is “called” as a function; if this method is defined, x(arg1, arg2, ...) is a shorthand
        for x.__call__(arg1, arg2, ...)


CONTAINER
---------

The collections.abc module provides a MutableMapping abstract base class to help create those methods from a base set of
__getitem__(), __setitem__(), __delitem__(), and keys(). Mutable sequences should provide methods append(), count(),
index(), extend(), insert(), pop(), remove(), reverse() and sort(), like Python standard list objects. Finally, sequence
types should implement addition (meaning concatenation) and multiplication (meaning repetition) by defining the methods
__add__(), __radd__(), __iadd__(), __mul__(), __rmul__() and __imul__() described below; they should not define other
numerical operators. It is recommended that both mappings and sequences implement the __contains__() method to allow
efficient use of the in operator; for mappings, in should search the mapping’s keys; for sequences, it should search
through the values. It is further recommended that both mappings and sequences implement the __iter__() method to allow
efficient iteration through the container; for mappings, __iter__() should iterate through the object’s keys; for
sequences, it should iterate through the values.


.. list-table:: CONTAINER TYPES
    :widths: 100 1500
    :header-rows: 1

    * - Name
      - Description

    * - __len__(self)
      - Called to implement the built-in function len(). Should return the length of the object, an integer >= 0. Also,
        an object that doesn’t define a __bool__() method and whose __len__() method returns zero is considered to be
        false in a Boolean context.

    * - __length_hint__(self)
      - Should return an estimated length for the object (which may be greater or less than the actual length). The
        length must be an integer >= 0. The return value may also be NotImplemented, which is treated the same as if the
        __length_hint__ method didn’t exist at all. This method is purely an optimization and is never required for
        correctness.

    * - __getitem__(self, key)
      - Called to implement evaluation of self[key]. For sequence types, the accepted keys should be integers and slice
        objects. Note that the special interpretation of negative indexes (if the class wishes to emulate a sequence
        type) is up to the __getitem__() method. If key is of an inappropriate type, TypeError may be raised; if of a
        value outside the set of indexes for the sequence (after any special interpretation of negative values),
        IndexError should be raised. For mapping types, if key is missing (not in the container), KeyError should be
        raised.

    * - __setitem__(self, key, value)
      - Called to implement assignment to self[key]. Same note as for __getitem__(). This should only be implemented for
        mappings if the objects support changes to the values for keys, or if new keys can be added, or for sequences if
        elements can be replaced. The same exceptions should be raised for improper key values as for the __getitem__()
        method.

    * - __delitem__(self, key)
      - Called to implement deletion of self[key]. Same note as for __getitem__(). This should only be implemented for
        mappings if the objects support removal of keys, or for sequences if elements can be removed from the sequence.
        The same exceptions should be raised for improper key values as for the __getitem__() method.

    * - __missing__(self, key)
      - Called by dict.__getitem__() to implement self[key] for dict subclasses when key is not in the dictionary.

    * - __iter__(self)
      - This method is called when an iterator is required for a container. This method should return a new iterator
        object that can iterate over all the objects in the container. For mappings, it should iterate over the keys of
        the container.

        Iterator objects also need to implement this method; they are required to return themselves. For more information
        on iterator objects. If a container supports different types of iteration, additional methods can be provided to
        specifically request iterators for those iteration types. (An example of an object supporting multiple forms of
        iteration would be a tree structure which supports both breadth-first and depth-first traversal.)

        The iterator objects themselves are required to support the following two methods, which together form the
        iterator protocol: __iter__() and __next__()

        * __iter__ : Return the iterator object itself. This is required to allow both containers and iterators to be used
          with the for and in statements.

        * __next__: Return the next item from the container. If there are no further items, raise the StopIteration
          exception. This method corresponds to the tp_iternext slot of the type structure for Python objects in the
          Python/C API.

    * - __reversed__(self)
      - Called (if present) by the reversed() built-in to implement reverse iteration. It should return a new iterator
        object that iterates over all the objects in the container in reverse order.

        If the __reversed__() method is not provided, the reversed() built-in will fall back to using the sequence
        protocol (__len__() and __getitem__()). Objects that support the sequence protocol should only provide
        __reversed__() if they can provide an implementation that is more efficient than the one provided by reversed().

    * - __contains__(self, item)
      - Called to implement membership test operators. Should return true if item is in self, false otherwise. For
        mapping objects, this should consider the keys of the mapping rather than the values or the key-item pairs.

        For objects that don’t define __contains__(), the membership test first tries iteration via __iter__(), then
        the old sequence iteration protocol via __getitem__().


CONTEXT MANAGER TYPE
--------------------

.. list-table:: CONTEXT MANAGER TYPE
    :widths: 500 1000
    :header-rows: 1

    * - Name
      - Description

    * - __enter__(self)
      - Enter the runtime context related to this object. The with statement will bind this method’s return value to the
        target(s) specified in the as clause of the statement, if any.

    * - __exit__(self, exc_type, exc_value, traceback)
      - Exit the runtime context related to this object. The parameters describe the exception that caused the context
        to be exited. If the context was exited without an exception, all three arguments will be None.

        If an exception is supplied, and the method wishes to suppress the exception (i.e., prevent it from being
        propagated), it should return a true value. Otherwise, the exception will be processed normally upon exit from
        this method.

        Note that __exit__() methods should not reraise the passed-in exception; this is the caller’s responsibility.



IMPORTANT
---------

.. topic:: **__slots__**

    A declaration inside a class that saves memory by pre-declaring space for instance attributes and eliminating instance
    dictionaries. Though popular, the technique is somewhat tricky to get right and is best reserved for rare cases where
    there are large numbers of instances in a memory-critical application.

.. note::

    #.  When inheriting from a class without __slots__, the __dict__ and __weakref__ attribute of the instances will
        always be accessible.

    #. Without a __dict__ variable, instances cannot be assigned new variables not listed in the __slots__ definition.
        Attempts to assign to an unlisted variable name raises AttributeError. If dynamic assignment of new variables
        is desired, then add '__dict__' to the sequence of strings in the __slots__ declaration.

    #. Without a __weakref__ variable for each instance, classes defining __slots__ do not support weak references to
       its instances. If weak reference support is needed, then add '__weakref__' to the sequence of strings in
       the __slots__ declaration.

    #. __slots__ are implemented at the class level by creating descriptors (Implementing Descriptors) for each variable
       name. As a result, class attributes cannot be used to set default values for instance variables defined by __slots__;
       otherwise, the class attribute would overwrite the descriptor assignment.

    #. The action of a __slots__ declaration is not limited to the class where it is defined. __slots__ declared in
       parents are available in child classes. However, child subclasses will get a __dict__ and __weakref__ unless
       they also define __slots__ (which should only contain names of any additional slots).

    #. If a class defines a slot also defined in a base class, the instance variable defined by the base class slot is
       inaccessible (except by retrieving its descriptor directly from the base class). This renders the meaning of the
       program undefined. In the future, a check may be added to prevent this.

    #. Nonempty __slots__ does not work for classes derived from “variable-length” built-in types such as int, bytes and
       tuple.

    #. Any non-string iterable may be assigned to __slots__. Mappings may also be used; however, in the future, special
       meaning may be assigned to the values corresponding to each key.

    #. __class__ assignment works only if both classes have the same __slots__.

    #. Multiple inheritance with multiple slotted parent classes can be used, but only one parent is allowed to have
       attributes created by slots (the other bases must have empty slot layouts) - violations raise TypeError.

    #. If an iterator is used for __slots__ then a descriptor is created for each of the iterator’s values. However,
       the __slots__ attribute will be an empty iterator.

.. topic:: **__hash__**

.. list-table::
    :widths: 100 1000
    :header-rows: 1

    * - Name
      - Description

    * - __hash__(self)
      - Called by built-in function hash() and for operations on members of hashed collections including set, frozenset,
        and dict. __hash__() should return an integer. The only required property is that objects which compare equal
        have the same hash value; it is advised to mix together the hash values of the components of the object that
        also play a part in comparison of objects by packing them into a tuple and hashing the tuple.


.. code-block:: python

    def __hash__(self):
        return hash((self.name, self.nick, self.color))


.. note::

    hash() truncates the value returned from an object’s custom __hash__() method to the size of a Py_ssize_t. This is
    typically 8 bytes on 64-bit builds and 4 bytes on 32-bit builds. If an object’s __hash__() must interoperate on
    builds of different bit sizes, be sure to check the width on all supported builds. An easy way to do this is with
    python -c "import sys; print(sys.hash_info.width)".

If a class does not define an __eq__() method it should not define a __hash__() operation either; if it defines __eq__()
but not __hash__(), its instances will not be usable as items in hashable collections. If a class defines mutable objects
and implements an __eq__() method, it should not implement __hash__(), since the implementation of hashable collections
requires that a key’s hash value is immutable (if the object’s hash value changes, it will be in the wrong hash bucket).

User-defined classes have __eq__() and __hash__() methods by default; with them, all objects compare unequal (except
with themselves) and x.__hash__() returns an appropriate value such that x == y implies both that x is y and hash(x)
== hash(y).

A class that overrides __eq__() and does not define __hash__() will have its __hash__() implicitly set to None. When
the __hash__() method of a class is None, instances of the class will raise an appropriate TypeError when a program
attempts to retrieve their hash value, and will also be correctly identified as unhashable when checking isinstance(obj,
collections.abc.Hashable).

If a class that overrides __eq__() needs to retain the implementation of __hash__() from a parent class, the interpreter
must be told this explicitly by setting __hash__ = <ParentClass>.__hash__.

If a class that does not override __eq__() wishes to suppress hash support, it should include __hash__ = None in the
class definition. A class which defines its own __hash__() that explicitly raises a TypeError would be incorrectly
identified as hashable by an isinstance(obj, collections.abc.Hashable) call.

.. note::

    By default, the __hash__() values of str and bytes objects are “salted” with an unpredictable random value. Although
    they remain constant within an individual Python process, they are not predictable between repeated invocations of Python.

    This is intended to provide protection against a denial-of-service caused by carefully-chosen inputs that exploit
    the worst case performance of a dict insertion, O(n^2) complexity. `See here <http://www.ocert.org/advisories/ocert-2011-003.html>`_ for details.

    Changing hash values affects the iteration order of sets. Python has never made guarantees about this ordering (and
    it typically varies between 32-bit and 64-bit builds).

    See also `PYTHONHASHSEED <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONHASHSEED>`_.

