import functools


def default_args(fun, **newkargs):
    """

    :param fun: original function
    :param newkargs: new args as default one of new function
    :return: fun with new default args
    """

    @functools.wraps(fun)
    def wrapped(*args, **kargs):
        for (k, v) in newkargs.items():
            kargs[k] = v
        return fun(*args, **kargs)

    return wrapped


