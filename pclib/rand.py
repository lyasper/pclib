import random, string, sys
import datetime

def randstr(length, digital=False, punctuation=False):
    if length <= 0:
        return ""
    strset = string.ascii_letters
    if digital:
        strset += string.digits
    if punctuation:
        strset += string.punctuation
    return ''.join(random.choice(strset) for i in range(length))


def randint(minvalue = None, maxvalue=None):
    if minvalue == None:
        minvalue = -sys.maxint - 1
    if maxvalue == None:
        maxvalue = sys.maxint
    if minvalue < maxvalue:
        return random.randint(minvalue, maxvalue)
    else:
        return random.randint(maxvalue, minvalue)

def randdate():
    # year = randint(datetime.MINYEAR, datetime.MAXYEAR)
    year = randint(1000, 2100)
    month = randint(1, 12)
    maxday = 28 if month == 2 else 30
    day = randint(1, maxday)
    hour = randint(0, 23)
    minute = randint(0, 59)
    second = randint(0, 59)
    microsecond = randint(0, 1000000-1)

    return datetime.datetime(year, month, day, hour, minute, second, microsecond)

def randipv4():
    return '.'.join(str(randint(0,255)) for x in xrange(4))

def randmac():
    hexdigits = '0123456789ABCDEF'
    return ':'.join(''.join(random.choice(hexdigits) for i in xrange(2)) for x in xrange(6))

class RandItem():
    _choices=set()
    def __init__(self, choices):
        self.expend(choices)
    def expend(self, choices):
        for i in choices:self._choices.add(i)
    def __call__(self):
        return random.choice(list(self._choices))

def main():
    r1 = RandItem(range(1024))
    for x in range(11):
        print randstr(256)
        print randint(100,999)
        print randdate()
        print randipv4()
        print randmac()
        print r1()

if __name__ == '__main__':
    #main()
    print randstr(1024)
