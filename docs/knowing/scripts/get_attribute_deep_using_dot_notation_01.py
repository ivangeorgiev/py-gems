import functools

def get_attr(obj, attr):
    return functools.reduce(getattr, attr.split('.'), obj)
