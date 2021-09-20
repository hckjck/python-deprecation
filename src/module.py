from warnings import warn

FOO = 'Foo'  # deprecated


# Accoding to PEP 562 (https://www.python.org/dev/peps/pep-0562/#id8), it does not work
def __getattr__(name):
    print(f'name: {name}')
    if name == 'FOO':
        warn(f'Constant {__name__}.FOO is deprecated.')

    try:
        return globals()[name]
    except AttributeError:
        raise
