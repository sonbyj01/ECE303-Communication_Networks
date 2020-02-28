#!/usr/bin/env python3

import sys
import getopt
import socket

# Checks if ports
def scan_ports(addrP, portsP = None):
    if portsP == None:
        port_range = ['1', '1024']
    else:
        port_range = portsP.split(':')
    remoteServerIP = socket.gethostbyname(addrP)  # performs a dns look up
    print("Checking from ports {} to {} on addr {}".format(port_range[0], port_range[1], remoteServerIP))

    try:
        for port in range(int(port_range[0]), int(port_range[1])):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remoteServerIP, port))
            if result == 0:
                print("Port {}: Open".format(port))
                sock.close()
    except KeyboardInterrupt:
        sys.exit()
    except socket.gaierror:
        print("issue with hostname")
        sys.exit()
    except socket.error:
        print("cant connect to server")
        sys.exit()

# main function
try:
    addr = str(sys.argv[1])
    print(addr)
    opts, args = getopt.getopt(sys.argv[2:], "p:")
    print(args)
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

# o == option
# a == argument passed to the o
# o, a = opts
print(opts)
a = None
scan_ports(addr, a)