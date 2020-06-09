#!/usr/bin/env python3
import sys
import getopt
import socket
import threading
import pyshark

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


def os_detection(address):
    capture = pyshark.RemoteCapture(address, 'wlo0')
    capture.sniff(timeout=50)


def tcp_connect(address, port, output):
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(10)
    try:
        TCPsock.connect((address, port))
        if str(port) in common_ports:
            output[port] = "Open:\t{} -> {}".format(str(port), common_ports[str(port)])
        else:
            output[port] = "Open:\t{}".format(str(port))
    except:
        output[port] = "Close:\t{}".format(str(port))
# making a fast port scanner 26174743 questions


def scan_ports(address, ports = None):
    if ports == None:
        port_range = ['1', '1024']
    else:
        port_range = ports.split(',')
    remote_server_ip = socket.gethostbyname(address)  # performs a dns look up
    print("Checking from ports {} to {} on addr {}".format(port_range[0], port_range[1], remote_server_ip))

    threads = []
    output = {}

    for port in range(int(port_range[0]), int(port_range[1])):
        t = threading.Thread(target=tcp_connect, args=(address, port, output))
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
def main():
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


if __name__ == '__main__':
    main()
