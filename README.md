# Python deprecation

As soon as you are developing a library, SDK or any other piece of code which is intended to be used by several people or software, you have to worry about how to introduce changes gracefully to your code over time.

The following document shows how to use deprecation in Python for different scenarios and parts of your code.

## How to use?

Under `./src` directory you are going to find examples including tests, showing how to deprecate and test your deprecations. By running them you can explore how it would behave at runtime. By opening it in your favourite IDE, you are able to check whether your IDE is supporting you by giving any hints when using deprecated stuff. You can run all tests using pytest.

## Throwing deprecation warnings

In order to throw warnings you want to use Pythons built in [warning control](https://docs.python.org/3/library/warnings.html).

```````python
from warnings import warn
```````

### Function deprecation

Deprecating a function is pretty easy just by using `warn` within a method like this.

```python
from warnings import warn

def a_deprecated_function():
    warn('This method is deprecated.', DeprecationWarning)
```

[Full example](./src/deprecate_function_test.py)

#### Deprecating function arguments

Deprecation on function arguments, requires you to check for your desired changes and throw `DeprecationWarning`'s withing the method.

```python
from warnings import warn

def a_function_with_deprecated_arguments(arg1, *args, kwarg1=None, **kwargs):
    # Positional argument `arg1` is going to change its type from (int, str) to (None, str)
    if type(arg1) is int:
        warn('`arg1` of type int is going to be deprecated.', DeprecationWarning)

    # Keyword argument `kwarg2` is going to be dropped completely.
    if 'kwarg2' in kwargs.keys():
        warn('kwarg2 will be deprecated.', DeprecationWarning)
```

[Full example](./src/deprecate_function_arguments_test.py)

## Class deprecation

When deprecating classes you have to consider two seperate use cases. Instantiating an object of a deprecated class can throw a deprecation warning by overriding the `__init__` method. In order to throw a warning on subclassing from a deprected method, you have to override the `__init_sublcall__` method instead.

```python
from warnings import warn

class ADeprecatedClass(object):
  
    def __init_subclass__(cls, **kwargs):
        """This throws a deprecation warning on subclassing."""
        warn(f'{cls.__name__} will be deprecated in v1.0.0', DeprecationWarning)
        super().__init_subclass__(**kwargs)

    def __init__(self, *args, **kwargs):
        """This throws a deprecation warning on initialization."""
        warn(f'{self.__class__.__name__} will be deprecated in v1.0.0', DeprecationWarning)
        super().__init__(*args, **kwargs)
```

[Full example](./src/deprecate_class_test.py)

### Deprecating a class method

Class method deprecation basicaly follows the same rules as [function deprecation](#function deprecation).

[Full example](./src/deprecate_class_method_test.py)

### Deprecating class variables

In order to deperecate class variables, you need to hook into `__getattribute__` method of objects metaclass.

```python
from warnings import warn

class DeprecatedMetaclass(type):

    def __getattribute__(self, item):
        if 'a_deprecated_class_variable' == item:
            warn(f'`{item}` class variable is deprecated')

        return type.__getattribute__(self, item)


class AClass(object, metaclass=DeprecatedMetaclass):
    a_class_variable = 'foo'
    a_deprecated_class_variable = None  # deprecated
```

[Full example](./src/deprecate_class_variables_test.py)

### Deprecating enum values

Due to the fact that enum values will be class variables of a subclass of Enum, the deprecation follows the same approach as [deprecating class variables](#Deprecating class variables) does.

```python
from enum import EnumMeta, Enum
from warnings import warn

class ADeprecatedEnumMeta(EnumMeta):

    def __getattribute__(self, item):
        if item == 'BAR':
            warn('BAR is going to be deprecated')
        return EnumMeta.__getattribute__(self, item)


class ADeprecatedEnum(Enum, metaclass=ADeprecatedEnumMeta):
    FOO = 'foo'
    BAR = 'bar'
```

[Full example](./src/deprecate_enum_value_test.py)

## Module deprecation

*TODO*

### Deprecating variables and constants on module level



```python

```

[Full example](./src/deprecate_module_variables_test.py)

### Testing deprecations



```python

```



## Documenting deprecations

*TODO*

## Maintaining deprecations

*TODO*

# Notes

Python provides a built-in integration between the `logging` module and the `warnings` module to let you do this; just call [`logging.captureWarnings(True)`](https://docs.python.org/library/logging.html#logging.captureWarnings) at the start of your script and all warnings emitted by the `warnings` module will automatically be logged at level `WARNING`.

https://code-examples.net/en/q/926881

---

Python warning control https://docs.python.org/3.5/library/warnings.html

---



