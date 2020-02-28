#!/usr/bin/env python3

import sys
import getopt
import socket
import threading

# Checks if ports
# def scan_ports(addrP, portsP = None):
#     if portsP == None:
#         port_range = ['1', '1024']
#     else:
#         port_range = portsP.split(',')
#     remoteServerIP = socket.gethostbyname(addrP)  # performs a dns look up
#     print("Checking from ports {} to {} on addr {}".format(port_range[0], port_range[1], remoteServerIP))
#     try:
#         for port in range(int(port_range[0]), int(port_range[1])):
#             print(port)
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             result = sock.connect_ex((remoteServerIP, port))
#             if result == 0:
#                 print("Port {}: Open".format(port))
#                 sock.close()
#     except KeyboardInterrupt:
#         sys.exit()
#     except socket.gaierror:
#         print("issue with hostname")
#         sys.exit()
#     except socket.error:
#         print("cant connect to server")
#         sys.exit()

def TCP_connect(addrP, portP, outputP):
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(10)
    try:
        TCPsock.connect((addrP, portP))
        outputP[portP] = "Open:\t" + str(portP)
    except:
        outputP[portP] = "Close:\t" + str(portP)
# making a fast port scanner 26174743 questions

def scan_ports(addrP, portsP = None):
    if portsP == None:
        port_range = ['1', '1024']
    else:
        port_range = portsP.split(',')
    remoteServerIP = socket.gethostbyname(addrP)  # performs a dns look up
    print("Checking from ports {} to {} on addr {}".format(port_range[0], port_range[1], remoteServerIP))

    threads = []
    output = {}

    for port in range(int(port_range[0]), int(port_range[1])):
        t = threading.Thread(target=TCP_connect, args=(addrP, port, output))
        threads.append(t)

    for i in range(int(port_range[1]) - int(port_range[0])):
        threads[i].start()

    for i in range(int(port_range[1]) - int(port_range[0])):
        threads[i].join()

    # for key in output:
    #     print(output[key])
    for port in range(int(port_range[0]), int(port_range[1])):
        print(output[port])

## main function
# checks to see if user input hostname/ip address argument
try:
    addr = str(sys.argv[1])
    print("Checking {}".format(addr))
except:
    print("You need a hostname or IP address!")
    sys.exit()

# checks to see if the user gave a specific port range
try:
    opts, args = getopt.getopt(sys.argv[2:], "p:")
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

try:
    o, a = opts[0]
except:
    o = None
    a = None

scan_ports(addr, a)
