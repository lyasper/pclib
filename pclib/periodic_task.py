import pyev
from copy import copy
import signal
import logging, threading
logging.basicConfig(level=logging.DEBUG)
from utils import full_stack
from multiprocessing import Process

_tasks=[]

def periodic(interval, *args, **kargs):
    def wrapper(f):
        if not callable(f):
            raise RuntimeError("{0} isn't callable".format(f))
        localloop = pyev.Loop()
        def timer_cb(watcher, revents):
            try:
                f(*args, **kargs)
            except:
                print full_stack()
        localtimer = localloop.timer(0, interval, timer_cb)
        class ThreadingTask(threading.Thread):
            def run(self):
                localtimer.start()
                localloop.start()
        _tasks.append((ThreadingTask(), localloop))
        return None
    return wrapper

def start_periodic_tasks():

    loop = pyev.default_loop(pyev.EVFLAG_FORKCHECK)
    def sig_cb(watcher, revents):
        loop.stop(pyev.EVBREAK_ALL)
        for t, l in _tasks:
            l.stop(pyev.EVBREAK_ALL)
            # t.join()
    for t,l in _tasks:
        t.start()
    # now wait for events to arrive
    sig = loop.signal(signal.SIGINT, sig_cb)
    sig.start()
    loop.start()


def main():
    @periodic(1,"earth")
    def test(s):
        import time
        time.sleep(10)
        print "hello, " +  str(s)

    @periodic(0.5)
    def test2():
        print "hello, world2"

    @periodic(3)
    def test3():
        print "hello, world3"

    start_periodic_tasks()

if __name__ == '__main__':
    main()
