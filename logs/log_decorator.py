import logging
import inspect

fmt = logging.Formatter(fmt='%(asctime)s %(message)s')
fh = logging.FileHandler(
    filename='logs/calls.log'
)
fh.setFormatter(fmt)
fh.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
calls = logging.getLogger('calls')
calls.addHandler(sh)
calls.addHandler(fh)


def log(func):
    def decorated(*args, **kwargs):
        res = func(*args, **kwargs)
        # print(f'{func.__name__}({args}, {kwargs}) = {res}')
        calls.debug('Функция %s(%s,%s) вызвана из функции %s', func.__name__, args, kwargs, inspect.stack()[1][3])
        return res

    return decorated
