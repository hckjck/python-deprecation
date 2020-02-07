"""
The following example shows how to deprecate a function properly.
It shows as well, how to test such deprecation.

Supported IDE's:

    Name                Version     Supported
    -----------------------------------------
    Atom                3.40.0      No
    PyCharm             2019.3      Yes
    Sublime Text        3.2.2       No

"""
from warnings import catch_warnings, warn


def a_deprecated_function():
    """
    A function which throws a DeprecationWarning with a particular reason.
    """
    warn('This method is deprecated, use `a_function` instead.', DeprecationWarning)


def test_a_deprecated_function():
    with catch_warnings(record=True) as w:
        a_deprecated_function()

        assert str(w[0].message) == 'This method is deprecated, use `a_function` instead.'
        assert len(w) == 1


if __name__ == '__main__':
    a_deprecated_function()
