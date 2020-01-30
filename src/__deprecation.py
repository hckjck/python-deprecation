import inspect
import logging
from enum import EnumMeta, Enum
from warnings import warn, catch_warnings

__VERSION__ = '1.3.0'

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class DeprecationWarning130(DeprecationWarning):
    pass


def a_method():
    """A regular method without any deprecation warning."""
    cur_frame = inspect.currentframe()
    cal_frame = inspect.getouterframes(cur_frame, 2)
    print(f'{cal_frame[1][3]} was called.')


# How to deprecate variables and constants on module level?
# #########################################################

# 1. try
# def deprecated(val, msg=None):
#     if not msg:
#         msg = 'This is deprecated.'
#     warn(msg, DeprecationWarning, 2)
#     return val
#
#
# a_deprecated_variable = deprecated(None, 'The variable `a_deprecated_variable` is deprecated without any replacement.')

# 2. try
a_deprecated_variable = None


# How to deprecate methods?
# #########################

def a_deprecated_mdethod():
    """
    A method which throws a DeprecationWarning with a particular reason.

    IDE support: yes

    """
    # warn('This mehtod is deprecated, use `a_method` instead.', DeprecationWarning)
    warn('This mehtod is deprecated, use `a_method` instead.', DeprecationWarning)
    a_method()


def a_method_with_deprecated_arguments(arg1, *args, kwarg1=None, **kwargs):
    """
    The following example shows how to deprecate method parameters.

    When changing signature of a method, I would recommend to deprecate the entire method. But still there will be cases
    where you want to deprecate a parameter or for example the support of an argument type.

    IDE support: no

    """
    # Positional argument `arg1` is going to change its type from (int, str) to (None, str)
    if type(arg1) is int:
        warn('arg1 of type int is going to be deprecated in v1.0.0', DeprecationWarning)

    # Keyword argument `kwarg2` is going to be dropped completely.
    if 'kwarg2' in kwargs.keys():
        warn('kwarg2 will be deprecated in v1.0.0', DeprecationWarning)

    a_method()


# How to deprecate classes?
# #########################

class ADeprecatedClass(object):
    """
    A class with throws deprecation warning on intialization.

    IDE support: yes, but not for subclasses
    """

    def __init_subclass__(cls, **kwargs):
        """This throws a deprecation warning on subclassing."""
        warn(f'{cls.__name__} will be deprecated in v1.0.0', DeprecationWarning)
        super().__init_subclass__(**kwargs)

    def __init__(self, *args, **kwargs):
        """This throws a deprecation warning on initialization."""
        warn(f'{self.__class__.__name__} will be deprecated in v1.0.0', DeprecationWarning)
        super().__init__(*args, **kwargs)


# How to deprecate class variables?
# #################################

class DeprecatedMetaclass(type):

    def __getattribute__(self, item):
        if item == 'foobar':
            warn('foobar is going to be deprecated in v1.0.0')
        return type.__getattribute__(self, item)


class AClassWithDeprecatedVariables(object, metaclass=DeprecatedMetaclass):
    foo = 'foo'
    bar = 'bar'
    foobar = None  # Deprecated


# Hot to deprecate enums?
# #######################

class ADeprecatedEnumMeta(EnumMeta):

    def __getattribute__(self, item):
        if item == 'BAR':
            warn('BAR is going to be deprecated by v2.0.0')
        return EnumMeta.__getattribute__(self, item)


class ADeprecatedEnum(Enum, metaclass=ADeprecatedEnumMeta):
    FOO = 'foo'
    BAR = 'bar'


if __name__ == '__main__':
    # Usage of deprecated module
    # with catch_warnings(record=True) as w:
    #     import pythonpackage.deprecated_module
    #     https://www.python.org/dev/peps/pep-0562/
    #     1. Deprecation warning on module import is shown in IDE properly
    #     2. Deprecation warning is thrown when running with `python -W default` only
    #     3. FIXME: `catch_warnings` does not catch
    #     assert str(w[0].message) == ''
    #     assert len(w) == 1

    # Usage of deprecated methods on module level
    # -------------------------------------------
    # with catch_warnings(record=True) as w:
    #     _ = a_deprecated_variable
    #     assert str(w[0].message) == ''
    #     assert len(w) == 1
    #
    # print('\nModule deprecation OK.')

    # Usage of deprecated methods
    # ---------------------------
    with catch_warnings(record=True) as w:
        a_deprecated_mdethod()
        assert str(w[0].message) == 'This mehtod is deprecated, use `a_method` instead.'
        assert len(w) == 1

    with catch_warnings(record=True) as w:
        a_method_with_deprecated_arguments(None)
        a_method_with_deprecated_arguments('foo')
        a_method_with_deprecated_arguments(1)
        assert str(w[0].message) == 'arg1 of type int is going to be deprecated in v1.0.0'

        a_method_with_deprecated_arguments(None, kwarg1=None, kwarg3=None)
        a_method_with_deprecated_arguments(None, kwarg2='foo')
        assert str(w[1].message) == 'kwarg2 will be deprecated in v1.0.0'
        assert len(w) == 2

    print('\nMethod deprecation OK.')

    # Usage of deprecated classes
    # ---------------------------
    with catch_warnings(record=True) as w:
        ADeprecatedClass()
        assert str(w[0].message) == 'ADeprecatedClass will be deprecated in v1.0.0'
        assert len(w) == 1

    with catch_warnings(record=True) as w:
        class AnotherDeprecatedClass(ADeprecatedClass):
            pass


        assert str(w[0].message) == 'AnotherDeprecatedClass will be deprecated in v1.0.0'

        AnotherDeprecatedClass()
        assert str(w[1].message) == 'AnotherDeprecatedClass will be deprecated in v1.0.0'
        assert len(w) == 2

    print('\nClass deprecation OK.')

    # Usage of deprecated class variables
    # -----------------------------------
    with catch_warnings(record=True) as w:
        _ = AClassWithDeprecatedVariables.foo
        _ = AClassWithDeprecatedVariables.bar
        _ = AClassWithDeprecatedVariables.foobar
        assert str(w[0].message) == 'foobar is going to be deprecated in v1.0.0'
        assert len(w) == 1

    print('\nClass variable deprecation OK.')

    # Usage of deprecated Enums
    # -------------------------
    with catch_warnings(record=True) as w:
        _ = ADeprecatedEnum.BAR.value
        _ = ADeprecatedEnum.FOO
        assert str(w[0].message) == 'BAR is going to be deprecated by v2.0.0'
        assert len(w) == 1

    print('\nEnum deprecation OK.')

    print("\nAll OK.")
