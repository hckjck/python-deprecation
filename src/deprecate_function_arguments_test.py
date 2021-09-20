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
        warn('arg1 of type int is deprecated', DeprecationWarning, stacklevel=2)

    # Keyword argument `kwarg2` is going to be dropped completely.
    if 'kwarg2' in kwargs.keys():
        warn('kwarg2 is deprecated', DeprecationWarning, stacklevel=2)


def test_a_function_with_deprecated_arguments():
    with catch_warnings(record=True) as w:
        a_function_with_deprecated_arguments(None)
        a_function_with_deprecated_arguments('foo')
        a_function_with_deprecated_arguments(1)
        assert len(w) == 1

        w0 = w[0]
        assert str(w0.message) == 'arg1 of type int is deprecated'
        assert issubclass(w0.category, DeprecationWarning)
        assert w0.filename == __file__

        a_function_with_deprecated_arguments(None, kwarg1=None, kwarg3=None)
        a_function_with_deprecated_arguments(None, kwarg2='foo')
        assert len(w) == 2

        w1 = w[1]
        assert str(w1.message) == 'kwarg2 is deprecated'
        assert issubclass(w1.category, DeprecationWarning)
        assert w1.filename == __file__


if __name__ == '__main__':
    a_function_with_deprecated_arguments(1, kwarg2='foo')
