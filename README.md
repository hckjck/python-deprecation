# Python deprecation

As soon as you are developing a library, SDK or any other piece of code, which is intended to be used by several people or software, you should think about _deprecation_.

> How to introduce changes gracefully to your code over time?

The following document shows how to use deprecation in Python for different scenarios and parts of your code using Python standard libraries.

It shows how to test deprecations and ensure warnings will be raised when you expect them to raise. 

Also, the topic of versioning deprecations will be covered, as well how to properly document them. 

Finally, we want to evaluate how to maintain deprecations from the point of view of a developer over time efficiently.

## How to use this project?

Under [`./src`](./src) directory you will find examples including tests, showing how to deprecate certain parts of your code and how to test them accordingly. 

Running `python deprecate_<example>_test.py` shows how a particular deprecation behaves at runtime. 

Open in your favorite IDE in order to check, if it is supporting you by giving hints, in case of using deprecated parts of your code.

Run all test using [pytest](https://docs.pytest.org) simply by `pytest`.

## Throwing deprecation warnings

The following section shows, how to use deprecation warnings in different parts of your code.

In order to throw warnings, you want to use Python's built in [warning control](https://docs.python.org/3/library/warnings.html).

```````python
from warnings import warn

warn('This is deprecated', DeprecationWarning, stacklevel=2)
```````

To warn about deprecation, you need to set Python's builtin `DeprecationWarning` as category. To let the warning refer to the caller, so you know exactly where you use deprecated code, you have to set `stacklevel=2`.

### Function deprecation

Deprecating a function is pretty easy just by using `warn` within a function like this.

```python
from warnings import warn

def a_deprecated_function():
    warn('This method is deprecated.', DeprecationWarning, stacklevel=2)
```

[Full example](./src/deprecate_function_test.py)

#### Deprecating function arguments

Deprecation on function arguments, requires you to check for your desired changes and throw `DeprecationWarning`'s withing the method.

```python
from warnings import warn

def a_function_with_deprecated_arguments(arg1, *args, kwarg1=None, **kwargs):
    # Positional argument `arg1` is going to change its type from (int, str) to (None, str)
    if type(arg1) is int:
        warn('arg1 of type int is going to be deprecated', DeprecationWarning, stacklevel=2)

    # Keyword argument `kwarg2` is going to be dropped completely.
    if 'kwarg2' in kwargs.keys():
        warn('kwarg2 will be deprecated', DeprecationWarning, stacklevel=2)
```

[Full example](./src/deprecate_function_arguments_test.py)

### Class deprecation

When deprecating classes you have to consider two seperate use cases. Instantiating an object of a deprecated class can throw a deprecation warning by overriding the `__init__` method. In order to throw a warning on subclassing from a deprected method, you have to override the `__init_sublcall__` method instead.

```python
from warnings import warn

class ADeprecatedClass(object):
  
    def __init_subclass__(cls, **kwargs):
        """This throws a deprecation warning on subclassing."""
        warn(f'{cls.__name__} will be deprecated.', DeprecationWarning, stacklevel=2)
        super().__init_subclass__(**kwargs)

    def __init__(self, *args, **kwargs):
        """This throws a deprecation warning on initialization."""
        warn(f'{self.__class__.__name__} will be deprecated.', DeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)
```

[Full example](./src/deprecate_class_test.py)

#### Deprecating a class method

Class method deprecation basicaly follows the same rules as [function deprecation](#function deprecation).

[Full example](./src/deprecate_class_method_test.py)

#### Deprecating class variables

In order to deperecate class variables, you need to hook into `__getattribute__` method of objects metaclass.

```python
from warnings import warn

class DeprecatedMetaclass(type):

    def __getattribute__(self, item):
        if 'a_deprecated_class_variable' == item:
            warn(f'{item} class variable is deprecated', DeprecationWarning, stacklevel=2)

        return type.__getattribute__(self, item)


class AClass(object, metaclass=DeprecatedMetaclass):
    a_class_variable = 'foo'
    a_deprecated_class_variable = None  # deprecated
```

[Full example](./src/deprecate_class_variables_test.py)

#### Deprecating enum values

Due to the fact that enum values will be class variables of a subclass of Enum, the deprecation follows the same approach as [deprecating class variables](#Deprecating class variables) does. In contrast you have to return the `EnumMeta.__getattribute__` as a super call instead, as you are subclassing from `EnumMeta`.

```python
from enum import EnumMeta, Enum
from warnings import warn

class ADeprecatedEnumMeta(EnumMeta):

    def __getattribute__(self, item):
        if item == 'BAR':
            warn('BAR is going to be deprecated', DeprecationWarning, stacklevel=2)
        return EnumMeta.__getattribute__(self, item)


class ADeprecatedEnum(Enum, metaclass=ADeprecatedEnumMeta):
    FOO = 'foo'
    BAR = 'bar'  # deprecated
```

[Full example](./src/deprecate_enum_value_test.py)

### Module deprecation

In order to deprecate a entire module just place a deprecation wraning at the top level of that module.

```python
# lib.py
from warnings import warn

warn(f'The module {__name__} is deprecated.', DeprecationWarning, stacklevel=2)
```

[Full example](./src/deprecate_module_test.py)

#### Deprecating variables and constants on module level

*TODO*

```python

```

[Full example](./src/deprecate_module_variables_test.py)

### Package deprecation

Package deprecation works the same way as [module deprecation](#Module deprecation), where the top level will be your `__init__.py` of the package to be deprecated.

[Full example](./src/deprecate_package_test.py)

## Testing deprecations

Python's [warning control](https://docs.python.org/3.5/library/warnings.html) provides a method called [catch_warnings](https://docs.python.org/3.5/library/warnings.html#warnings.catch_warnings) to collect warnings within a `with` block. Setting `record=True` enables you to record the warnings which were emittied during execution of your code and check if the desired warnings where raised as expected. We won't evalutate this in depth, due to it is well documentent in Python documentation [here](https://docs.python.org/3.5/library/warnings.html#testing-warnings).

```python
from warnings import catch_warnings

def test_a_deprecated_enum_value():
    with catch_warnings(record=True) as w:
      	# ADeprecatedEnum.FOO is not deprecated and should not throw any warning
        ADeprecatedEnum.FOO
        assert len(w) == 0

        # ADeprecatedEnum.BAR is deprecated and we expect to have a warning raised.
        ADeprecatedEnum.BAR
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert str(w[0].message) == 'BAR is deprecated'

```

Have a look under [`./src`](./src) directory for more examples on testing.

## Versioning deprecations

Deprecation messages make most sense, when they also provide information, when a particular deprecation is intended to become active. Depending on your deprecation policy and your release cycles you can have deprecation tied to a version or a particular point in time.

Decide on a message format, for example `message; key=value`. This way, adding meta information is straight forward and can be parsed by other tools easily as well.

```python
from warnings import warn

warn("This is deprecated; version=1.0.0", DeprecationWarning, stacklevel=2)
```

Use common keywords like `version` or `date` for indicating changes in a particular point in time.

```python
from warnings import warn

warn("This is deprecated; date=2022-01-01", DeprecationWarning, stacklevel=2)
```

## Documenting deprecations

*TODO: Evaluate how to prpoerly document deprecations*

> - Pydoc: https://docs.python.org/3.7/librxary/pydoc.html
> - Epydoc: http://epydoc.sourceforge.net/epydoc.html `@deprecated: ...`
> - Sphynx: https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-deprecated `.. deprecated:: version`

## Maintaining deprecations

*TODO: Evaluate how to maintain deprecation from a developer perspective over time*

> - As a developer I would like to have an easy way to collect all deprecations of my source code as a list, so I'm able to provide this to the public
> - As a developer I would like to let my tests fail in case there is a deprecation in my source code which version maches the current version of my software, so I'm able to get rid of the warning and finally deprecate

## Third party libraries

*TODO: Evaluate existing third party libraries covering the topic deprecation*

> - https://pypi.org/project/pytest-deprecate/
> - https://pypi.org/project/deprecate/
> - https://pypi.org/project/deprecationlib/
> - https://pypi.org/project/Deprecated/
> - https://pypi.org/project/Python-Deprecated/
> - https://pypi.org/project/libdeprecation/
> - https://pypi.org/project/deprecation/
> - https://pypi.org/project/pytest-deprecatde/

# Summary and outlook, conclusion?

*TODO*

# Notes

Python provides a built-in integration between the `logging` module and the `warnings` module to let you do this; just call [`logging.captureWarnings(True)`](https://docs.python.org/library/logging.html#logging.captureWarnings) at the start of your script and all warnings emitted by the `warnings` module will automatically be logged at level `WARNING`.

https://code-examples.net/en/q/926881

---

[Python warning control](https://docs.python.org/3.5/library/warnings.html)

---

[PEP 565 -- Show DeprecationWarning in  `__main__`](https://www.python.org/dev/peps/pep-0565/)

---

How this project or document could be improved to provide even more?

- by providing some more python background information, how python works and meta programming...?

