"""
The following example shows how to deprecate an entire class.

Supported IDE's:

    Name                Version     Supported
    -----------------------------------------
    Atom                3.40.0      No
    PyCharm             2019.3      Yes
    Sublime Text        3.2.2       No

"""
from warnings import warn, catch_warnings


class ADeprecatedClass(object):
    """
    A class which throws deprecation warning on initialization.

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


def test_a_deprecated_class():
    with catch_warnings(record=True) as w:
        ADeprecatedClass()
        assert str(w[0].message) == 'ADeprecatedClass will be deprecated in v1.0.0'
        assert len(w) == 1

    with catch_warnings(record=True) as w:
        class ADeprecatedSubclass(ADeprecatedClass):
            """No hint in PyCharm 2019.3 about the usage of an deprecated class as base."""
            pass

        # a deprecation warning will be thrown at runtime when using as base
        assert str(w[0].message) == 'ADeprecatedSubclass will be deprecated in v1.0.0'

        # a second deprecation will be thrown at runtime at initialization.
        ADeprecatedSubclass()
        assert str(w[0].message) == 'ADeprecatedSubclass will be deprecated in v1.0.0'
        assert len(w) == 2


if __name__ == '__main__':
    # The following line will be marked as deprecated in PyCharm 2019.3
    ADeprecatedClass()

    # # ...while ADeprecatedSubclass which is a subclass of ADeprecatedClass, won't.
    # ADeprecatedSubclass()
