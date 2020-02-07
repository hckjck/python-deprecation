"""
The following example shows how to deprecate variables on package level.
It shows as well, how to test such deprecation.

Supported IDE's:

    Name                Version     Supported
    -----------------------------------------
    Atom                3.40.0      No
    PyCharm             2019.3      No
    Sublime Text        3.2.2       No

"""
from unittest import skip
from warnings import catch_warnings, warn


@skip('broken')
def test_a_deprecated_variable():
    with catch_warnings(record=True) as w:
        from module import FOO
        assert len(w) == 1

        w0 = w[0]
        assert str(w0.message) == 'The variable FOO is deprecated'
        assert issubclass(w0.category, DeprecationWarning)
        assert w0.filename == __file__


if __name__ == '__main__':
    from module import FOO
    print(FOO)
