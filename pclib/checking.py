from shcmd import syncexec as RUN
import os, time, os.path


def is_host_available(hostaddr):
    if not hostaddr:
        return False
    cmd = "ping -c 1 -w 3 {host}".format(host=hostaddr)
    r = RUN(cmd)
    return True if r else False

def is_port_open(host, port):
    if not host or not port:
        return False
    cmd = "nc -z {host} {port}-{port}".format(host=host, port=port)
    r = RUN(cmd)
    return True if r else False


def is_file_exist(path):
    return os.access(path, os.F_OK)

def wait_for_host_ready(hostaddr, timeout=0):
    if not hostaddr:
        return False
    cmd = "ping -c 1 -w 1 {host}".format(host=hostaddr)
    r = None
    if timeout == 0:
        timeout = 1000000
    while timeout > 0:
        r = RUN(cmd)
        if r:
            break
        else:
            timeout -= 1
        time.sleep(1)
    return True if r else False

def wait_for_service_ready(hostaddr, port, timeout=0):
    if timeout == 0:
        timeout = 1000000
    r = False
    while timeout > 0:
        r = is_port_open(hostaddr, port)
        if r:
            break
        else:
            timeout -= 1
        time.sleep(1)
    return True if r else False

def test():
    print is_host_available("127.0.0.1")
    wait_for_host_ready("127.0.0.1")
    print is_file_exist("/home/xeven/")
    wait_for_service_ready("127.0.0.1", 8888)


if __name__ == '__main__':
    test()
