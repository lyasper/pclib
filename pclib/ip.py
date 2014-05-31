__author__ = 'lij55'

import socket, struct

from pyparsing import Suppress, Word, Combine, ZeroOrMore, \
    nums, hexnums, alphanums, printables, lineStart
from cmd import runcmd

def getlocalip():
    '''
    through dns
    '''
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def parseipaddr_osx(text):
    LBRACE,RBRACE,SEMI,QUOTE,COLO = map(Suppress,'{};":')
    ipAddress = Combine(Word(nums) + ('.' + Word(nums))*3)
    hexint = Word(hexnums,exact=2)
    macAddress = Combine(hexint + (':'+hexint)*5)

    ifaceName = Word(alphanums)
    ignore = Suppress(Word(printables + ' '))

    ethline =  Suppress("ether") + macAddress
    optline = Suppress("options") + ignore
    header =  lineStart + ifaceName + COLO + ignore
    ipv4line =   Suppress("inet") + ipAddress

    patt =  header + ZeroOrMore(optline) + ethline + ipv4line
    items = patt.searchString(text)
    return items[0].dump()


def getinterfaceip(interface):
    '''
    ifconfig
    '''
    if not interface: return None
    cmd = '/sbin/ifconfig {0!s}'.format(interface)
    (ret, out)  = runcmd(cmd)
    if(ret == 0):
        return parseipaddr_osx(out)
    else:
        return None



def makeMask(n):
    "return a mask of n bits as a long integer"
    return (2L << n - 1) - 1


def maskLen(mask):
    n = 1
    while (mask == ((mask >> n) << n)):
        n += 1
    return n - 1


def ip2int(addr_str):
    return struct.unpack("!I", socket.inet_aton(addr_str))[0]


def int2ip(addr_int):
    return socket.inet_ntoa(struct.pack("!I", addr_int))

if __name__ == "__main__":
    # print(getlocalip())
    print(ip2int("192.168.88.44"))
    print(ip2int("255.255.0.0"))
    print(int2ip(ip2int("192.168.88.44") & ip2int("255.255.0.0")))
    print(int2ip(0xffffff00))
    print getinterfaceip("en3")
    print getinterfaceip("lo")