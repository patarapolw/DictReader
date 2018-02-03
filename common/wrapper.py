from common import common


def iter2list(func):
    def wrapper(*args, **kwargs):
        return list(func(*args, **kwargs))
    return wrapper


def speedWrapper(func):
    def wrapper(*args, **kwargs):
        with common.speedTest(func.__qualname__):
            return func(*args, **kwargs)
    return wrapper
