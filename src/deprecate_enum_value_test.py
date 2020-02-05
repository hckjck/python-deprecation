"""
The following example shows how to deprecate enum values properly.
It shows as well, how to test such deprecation.

Supported IDE's:

    Name                Version     Supported
    -----------------------------------------
    Atom                3.40.0      No
    PyCharm             2019.3      No
    Sublime Text        3.2.2       No

"""
from enum import EnumMeta, Enum
from warnings import warn, catch_warnings


class ADeprecatedEnumMeta(EnumMeta):

    def __getattribute__(self, item):
        if item == 'BAR':
            warn('BAR is going to be deprecated')
        return EnumMeta.__getattribute__(self, item)


class ADeprecatedEnum(Enum, metaclass=ADeprecatedEnumMeta):
    FOO = 'foo'
    BAR = 'bar'  # deprecated


def test_a_deprecated_enum_value():
    with catch_warnings(record=True) as w:
        ADeprecatedEnum.FOO
        assert len(w) == 0

        ADeprecatedEnum.BAR
        assert str(w[0].message) == 'BAR is going to be deprecated'
        assert len(w) == 1


if __name__ == '__main__':
    ADeprecatedEnum.FOO
    ADeprecatedEnum.BAR
