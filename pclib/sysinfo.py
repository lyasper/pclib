import platform, socket

def ostype():
    return platform.system()
def arch():
    return platform.machine()

def hostname():
    return socket.gethostname()

def get_system_type():
    print platform.system()
    print platform.machine()
    print platform.mac_ver()
    print platform.win32_ver()
    print platform.linux_distribution()
    print platform.platform()

if __name__ == "__main__":
    get_system_type()
    print ostype()
    print arch()
    print hostname()