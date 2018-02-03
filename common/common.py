import collections
from time import time


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


class speedTest:
    def __init__(self, testName):
        self.funcName = testName

    def __enter__(self):
        print('Started: {}'.format(self.funcName))
        self.init_time = time()
        return self

    def __exit__(self, type, value, tb):
        print('Finished: {} in: {} seconds'.format(self.funcName, time() - self.init_time))
