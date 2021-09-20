"""
The following example shows how to deprecate a class method properly.
It shows as well, how to test such deprecation.

Supported IDE's:

    Name                Version     Supported
    -----------------------------------------
    Atom                3.40.0      No
    PyCharm             2019.3      Yes
    Sublime Text        3.2.2       No

"""
from warnings import catch_warnings, warn


class AClass(object):

    @staticmethod
    def a_deprecated_staticmethod():
        """
        A static method which throws a DeprecationWarning with a particular reason.
        """
        warn('This method is deprecated', DeprecationWarning, stacklevel=2)

    @classmethod
    def a_deprecated_classmethod(cls):
        """
        A class method which throws a DeprecationWarning with a particular reason.
        """
        warn('This method is deprecated', DeprecationWarning, stacklevel=2)

    def a_deprecated_method(self):
        """
        A method which throws a DeprecationWarning with a particular reason.
        """
        warn('This method is deprecated', DeprecationWarning, stacklevel=2)


def test_a_deprecated_staticmethod():
    with catch_warnings(record=True) as w:
        AClass.a_deprecated_staticmethod()
        assert len(w) == 1

        w0 = w[0]
        assert str(w0.message) == 'This method is deprecated'
        assert issubclass(w0.category, DeprecationWarning)
        assert w0.filename == __file__


def test_a_deprecated_classmethod():
    with catch_warnings(record=True) as w:
        AClass.a_deprecated_classmethod()

        assert len(w) == 1

        w0 = w[0]
        assert str(w0.message) == 'This method is deprecated'
        assert issubclass(w0.category, DeprecationWarning)
        assert w0.filename == __file__


def test_a_deprecated_method():
    with catch_warnings(record=True) as w:
        AClass().a_deprecated_method()

        assert len(w) == 1

        w0 = w[0]
        assert str(w0.message) == 'This method is deprecated'
        assert issubclass(w0.category, DeprecationWarning)
        assert w0.filename == __file__


if __name__ == '__main__':
    AClass.a_deprecated_classmethod()

    AClass.a_deprecated_staticmethod()

    AClass().a_deprecated_method()
