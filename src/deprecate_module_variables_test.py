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
from warnings import catch_warnings, warn


def test_a_deprecated_variable():
    with catch_warnings(record=True) as w:
        from module import FOO

        assert str(w[0].message) == 'The variable FOO is deprecated.'
        assert len(w) == 1


if __name__ == '__main__':
    from module import FOO
    print(FOO)
