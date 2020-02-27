#!/usr/bin/env python3

import sys
import getopt

def checkPorts(portsP = None):
    if portsP == None:
        pass
    else:
        a = portsP.split(':')
        print(a)

# assumes the hostname is the first argument
try:
    addr = str(sys.argv[1])
    opts, args = getopt.getopt(sys.argv[2:], "p:")
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)


print(addr)
# o == option
# a == argument passed to the o
for o, a in opts:
    if o == '-p':
        print(a)
        checkPorts(a)
    else:
        print("Usage: %s -i input -o output" % sys.argv[0])

