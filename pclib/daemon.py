#!/usr/bin/env python

import sys, os, time, atexit, os.path, logging
from signal import SIGTERM
import stdbuf
from functools import wraps


class Daemon:
    """
    A generic daemon class.
    
    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        
    
    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced 
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try: stdbuf.stdout_line()
        except: pass
        try: 
            pid = os.fork() 
            if pid > 0:
                # return from first parent
                sys.exit(0) 
        except OSError, e: 
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
    
        # decouple from parent environment
        os.chdir("/") 
        os.setsid() 
        os.umask(0) 
    
        # do second fork
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit from second parent
                sys.exit(0) 
        except OSError, e: 
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1) 
    
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        # sys.stdout.close()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'w+', 1)
        # sys.stdout = file(self.stdout, 'w+', 1)
        se = file(self.stderr, 'w+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)
    
    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
    
        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)
        
        # Start the daemon
        self.daemonize()
        # only run in child process
        if not pid:
            self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
    
        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart

        # Try killing the daemon process    
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """

def printfile(fine):
    with open(fine) as f: 
        for l in f: print l.rstrip()

def DaemonizeIt(longlivingfun):
    '''
    Trans function to a dameon
    '''
    @wraps(longlivingfun)
    def daemonwrap(*args, **kargv):
        path_prefix = "/var/log/" if os.getuid() == 0 else "/tmp/log/"
        fun_data_path = path_prefix + "daemon_{0}/".format(longlivingfun.func_name)
        try:
            os.mkdir(fun_data_path)
        except:
            pass
        idfile = fun_data_path + "pid"
        output = fun_data_path + "output.log"
        errlog = fun_data_path + "error.log"

        class WrappedDaemon(Daemon):
            def run(self):
                longlivingfun(*args, **kargv)

        daemon = WrappedDaemon(idfile, stdout=output, stderr=errlog)
        if len(sys.argv) >= 2:
            daemon_args = sys.argv.pop(1)
            if 'start' == daemon_args:
                daemon.start()
            elif 'stop' == daemon_args:
                daemon.stop()
            elif 'restart' == daemon_args:
                daemon.restart()
            elif 'status' == daemon_args:
                pid = None
                pf = None
                try:
                    pf = file(daemon.pidfile,'r')
                    pid = int(pf.read().strip())
                    # pf.close()
                except:
                    pass
                finally:
                    if pf:pf.close()
                if pid and os.path.exists("/proc/{0}".format(str(pid))):
                    f = open("/proc/{0}/cmdline".format(str(pid)))
                    cmd = f.readline()
                    # print cmd
                    if sys.argv[0] in cmd:
                        print "running with pid {}".format(str(pid))
                    else:
                        print "not running"
                else:
                    print "not running"
                    sys.exit(-1)
            elif 'log' == daemon_args:
                printfile(output)
            elif 'error' == daemon_args:
                printfile(errlog)
            elif 'pid' == daemon_args:
                printfile(idfile)
            elif 'nodaemon' == daemon_args:
                longlivingfun(*args, **kargv)
            else:
                print "Unknown command: {0}".format(daemon_args)
                print "usage: %s start|stop|restart|status|log|error|pid|nodaemon" % sys.argv[0]
                sys.exit(2)
            sys.exit(0)
        else:
            print "usage: %s start|stop|restart|status|log|error|pid|nodaemon" % sys.argv[0]
            sys.exit(2)
    return daemonwrap



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

def periodic_in_daemon(interval):
    from functools import wraps
    def wrapped_fun(fun):
        @DaemonizeIt
        @wraps(fun)
        def periodic_fun(*args, **kargs):
            while True:
                try:
                    fun(*args, **kargs)
                except Exception as e:
                    logging.fatal(str(e))
                    stack_log =  full_stack()
                    logging.fatal(str(stack_log))
                finally:
                    time.sleep(interval)
        return periodic_fun
    return wrapped_fun

if __name__ == "__main__":
    pass
    # test1()
    # test2()
