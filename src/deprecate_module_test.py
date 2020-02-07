"""
The following example shows how to deprecate an entire package.
It shows as well, how to test such deprecation.

Supported IDE's:

    Name                Version     Supported
    -----------------------------------------
    Atom                3.40.0      No
    PyCharm             2019.3      No
    Sublime Text        3.2.2       No

"""
from warnings import catch_warnings


def test_a_deprecated_function():
    with catch_warnings(record=True) as w:
        import deprecated_module

        assert str(w[0].message) == 'The module deprecated_module is deprecated.'
        assert len(w) == 1


if __name__ == '__main__':
    import deprecated_module
