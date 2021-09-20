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
        warn(f'{cls.__name__} is deprecated', DeprecationWarning, stacklevel=2)
        super().__init_subclass__(**kwargs)

    def __init__(self, *args, **kwargs):
        """This throws a deprecation warning on initialization."""
        warn(f'{self.__class__.__name__} is deprecated', DeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)


def test_a_deprecated_class():
    with catch_warnings(record=True) as w:
        ADeprecatedClass()
        assert len(w) == 1

        w0 = w[0]
        assert str(w0.message) == 'ADeprecatedClass is deprecated'
        assert issubclass(w0.category, DeprecationWarning)
        assert w0.filename == __file__

    with catch_warnings(record=True) as w:
        class ADeprecatedSubclass(ADeprecatedClass):
            """No hint in PyCharm 2019.3 about the usage of an deprecated class as base."""
            pass

        assert len(w) == 1

        # a deprecation warning will be thrown at runtime when using as base
        w0 = w[0]
        assert str(w0.message) == 'ADeprecatedSubclass is deprecated'
        assert issubclass(w0.category, DeprecationWarning)
        assert w0.filename == __file__

        # a second deprecation will be thrown at runtime on initialization.
        ADeprecatedSubclass()
        w1 = w[1]
        assert len(w) == 2
        assert str(w1.message) == 'ADeprecatedSubclass is deprecated'
        assert issubclass(w1.category, DeprecationWarning)
        assert w1.filename == __file__


if __name__ == '__main__':
    # The following line will be marked as deprecated in PyCharm 2019.3
    ADeprecatedClass()
