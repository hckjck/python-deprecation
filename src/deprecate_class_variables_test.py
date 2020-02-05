"""
The following example shows how to deprecate class variables properly.
It shows as well, how to test such deprecation.

Supported IDE's:

    Name                Version     Supported
    -----------------------------------------
    Atom                3.40.0      No
    PyCharm             2019.3      No
    Sublime Text        3.2.2       No

"""
from warnings import catch_warnings, warn


class DeprecatedMetaclass(type):

    def __getattribute__(self, item):
        if 'a_deprecated_class_variable' == item:
            warn(f'`{item}` class variable is deprecated')

        return type.__getattribute__(self, item)


class AClass(object, metaclass=DeprecatedMetaclass):
    a_class_variable = 'foo'
    a_deprecated_class_variable = None  # deprecated


def test_a_deprecated_staticmethod():
    with catch_warnings(record=True) as w:
        AClass.a_class_variable
        AClass.a_deprecated_class_variable

        assert str(w[0].message) == '`a_deprecated_class_variable` class variable is deprecated'
        assert len(w) == 1


if __name__ == '__main__':
    AClass.a_class_variable
    AClass.a_deprecated_class_variable
