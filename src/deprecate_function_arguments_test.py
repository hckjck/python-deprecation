"""
The following example shows how to deprecate function parameters.

When changing signature of a function, I would recommend to deprecate the entire function. But still there will be cases
where you want to deprecate a parameter or for example the support of an argument type.

Supported IDE's:

    Name                Version     Supported
    -----------------------------------------
    Atom                3.40.0      No
    PyCharm             2019.3      No
    Sublime Text        3.2.2       No

"""
from warnings import catch_warnings, warn


def a_function_with_deprecated_arguments(arg1, *args, kwarg1=None, **kwargs):
    """
    A function which throws a DeprecationWarning when deprecated arguments are used.
    """
    # Positional argument `arg1` is going to change its type from (int, str) to (None, str)
    if type(arg1) is int:
        warn('arg1 of type int is going to be deprecated in v1.0.0', DeprecationWarning)

    # Keyword argument `kwarg2` is going to be dropped completely.
    if 'kwarg2' in kwargs.keys():
        warn('kwarg2 will be deprecated in v1.0.0', DeprecationWarning)


def test_a_function_with_deprecated_arguments():
    with catch_warnings(record=True) as w:
        a_function_with_deprecated_arguments(None)
        a_function_with_deprecated_arguments('foo')
        a_function_with_deprecated_arguments(1)
        assert str(w[0].message) == 'arg1 of type int is going to be deprecated in v1.0.0'

        a_function_with_deprecated_arguments(None, kwarg1=None, kwarg3=None)
        a_function_with_deprecated_arguments(None, kwarg2='foo')
        assert str(w[1].message) == 'kwarg2 will be deprecated in v1.0.0'
        assert len(w) == 2


if __name__ == '__main__':
    a_function_with_deprecated_arguments(1, kwarg2='foo')
