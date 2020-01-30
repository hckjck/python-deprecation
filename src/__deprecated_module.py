from warnings import warn

# Deprecate the entire module
warn('Deprecated', DeprecationWarning)

a_deprecated_variable = None

#
# https://www.python.org/dev/peps/pep-0562/
#
# def __getattr__(name):
#     if name == 'a_deprecated_variable':
#         warn("That has been deprecated, use the new features!", DeprecationWarning)
#         return globals()['a_deprecated_variable']
#     raise AttributeError(f"module {__name__} has no attribute {name}")


deprecated_names = ["old_function"]


def _deprecated_old_function(arg, other):
    pass


def __getattr__(name):
    if name in deprecated_names:
        warn(f"{name} is deprecated", DeprecationWarning)
        return globals()[f"_deprecated_{name}"]
    raise AttributeError(f"module {__name__} has no attribute {name}")
