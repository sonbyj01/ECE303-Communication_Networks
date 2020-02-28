#! /usr/bin/env python3
import socket
import sys

from pip._vendor.distlib.compat import raw_input

remoteServer = raw_input("enter remote host to scan: ")
remoteServerIP = socket.gethostbyname(remoteServer)
print(remoteServerIP)
try:
    for port in range(1, 1025):
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