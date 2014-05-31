import datetime
import logging
from datetime import datetime
import traceback,sys
import pdb
from functools import wraps

def full_stack():
    import traceback, sys
    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    if not exc is None:  # i.e. if an exception is present
        del stack[-1]       # remove call of full_stack, the printed exception
                            # will contain the caught exception caller instead
    trc = 'Traceback (most recent call last):\n'
    stackstr = trc + ''.join(traceback.format_list(stack))
    if not exc is None:
         stackstr += '  ' + traceback.format_exc().lstrip(trc)
    return stackstr





def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    import time
    from functools import wraps
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck, e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print msg
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


def exception_to_false(f):
    def wrapped_f(*args, **kargs):
        try:
            return f(*args, **kargs)
        except:
            stacklog = full_stack()
            print stacklog
            return False
    return wrapped_f




_PERFECT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

def utcnow():
    """Overridable version of utils.utcnow."""
    return datetime.datetime.utcnow()


def strtime(at=None, fmt=_PERFECT_TIME_FORMAT):
    """Returns formatted utcnow."""
    if not at:
        at = utcnow()
    return at.strftime(fmt)


def parse_strtime(timestr, fmt=_PERFECT_TIME_FORMAT):
    """Turn a formatted time back into a datetime."""
    return datetime.datetime.strptime(timestr, fmt)


"""
UUID related utilities and helper functions.
From openstack
"""

import uuid


def generate_uuid():
    return str(uuid.uuid4())


def is_uuid_like(val):
    """Returns validation of a value as a UUID.

    For our purposes, a UUID is a canonical form string:
    aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa

    """
    try:
        return str(uuid.UUID(val)) == val
    except (TypeError, ValueError, AttributeError):
        return False


def TRACE(timed, verbose=False):
	#print ("timed is {0}, verbose is {1}".format(timed, verbose))
	def decorator(fun):
		def wrapped(*args, **kargs):
			if verbose: print("in {0}".format(fun.__name__))
			if timed:
				o = fun(*args,**kargs)
			else:
				o = fun(*args,**kargs)
			return o
		return wrapped
	return decorator

def dump_args(func):
    "This decorator dumps out the arguments passed to a function before calling it"
    argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
    fname = func.func_name
    @wraps(func)
    def echo_func(*args,**kwargs):
        print fname, ":", ', '.join(
            '%s=%r' % entry
            for entry in zip(argnames,args) + kwargs.items())
        return func(*args, **kwargs)

    return echo_func

class TimeFormatter(logging.Formatter):
	def formatTime(self,record, datefmt=None):
		dt = datetime.now()
		return "[{0}]".format(dt.strftime("%y%m%d-%H%M%S-%f"))

def getstack(msg=None):
	ret = "{0}\n>>>>>\n".format(msg)
	stacks = traceback.extract_stack()
	for s in stacks[:-1]:
		i = "{0:<16}{2:<8}{1:>5}|{3}\n".format(*s)
		ret += i
	return ret+"<<<<<<\n"


def benchmark(func):
    """
    A decorator that print the time of function take
    to execute.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t = time.time()
        res = func(*args, **kwargs)
        print func.__name__, time.time()-t
        return res
    return wrapper


def xlog(func):
    """
    A decorator that logs the activity of the script.
    (it actually just prints it, but it could be logging!)
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print func.__name__, args, kwargs
        return res
    return wrapper


def counter(func):
    """
    A decorator that counts and prints the number of times a function has been executed
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.count = wrapper.count + 1
        res = func(*args, **kwargs)
        print "{0} has been used: {1}x".format(func.__name__, wrapper.count)
        return res
    wrapper.count = 0
    return wrapper

if __name__ == '__main__':
    class xxx:
        pass
    @exception_to_false
    def testexceptiion():
        raise xxx()

    print testexceptiion()
