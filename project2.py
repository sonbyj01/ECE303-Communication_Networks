#!/usr/bin/env python3
import sys
import getopt
import socket
import threading

common_ports = {
    '21': 'ftp',
    '22': 'ssh',
    '23': 'telnet',
    '25': 'smtp',
    '53': 'domain name system',
    '80': 'http',
    '110': 'pop3',
    '111': 'rpcbind',
    '135': 'msrpc',
    '139': 'netbios.ssn',
    '143': 'imap',
    '443': 'https',
    '445': 'microsoft-ds',
    '993': 'imaps',
    '995': 'pop3s'
}

def TCP_connect(addrP, portP, outputP):
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(10)
    try:
        TCPsock.connect((addrP, portP))
        if str(portP) in common_ports:
            outputP[portP] = "Open:\t{} -> {}".format(str(portP), common_ports[str(portP)])
        else:
            outputP[portP] = "Open:\t{}".format(str(portP))
    except:
        outputP[portP] = "Close:\t{}".format(str(portP))
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

    for port in range(int(port_range[0]), int(port_range[1])):
        if "Open" in output[port]:
            print(output[port])


## main function
# checks to see if user input hostname/ip address argument
try:
    address = str(sys.argv[1])
    print("Checking {}".format(address))
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

scan_ports(address, a)
