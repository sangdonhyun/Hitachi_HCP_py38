# SuperFastPython.com
# scan a range of port numbers on host one by one
from socket import AF_INET
from socket import SOCK_STREAM
from socket import socket


# returns True if a connection can be made, False otherwise
def test_port_number(host, port):
    # create and configure the socket
    # print(host,port)
    with socket(AF_INET, SOCK_STREAM) as sock:
        # set a timeout of a few seconds
        sock.settimeout(3)
        # connecting may fail
        try:
            # attempt to connect
            sock.connect((host, port))
            # a successful connection was made
            return True
        except Exception as e:
            # print(str(e))
            # ignore the failure
            return False


# scan port numbers on a host
def port_scan(host, ports):
    print(f'Scanning {host}...')
    # scan each port number
    for port in ports:
        if test_port_number(host, port):
            print(f'> {host}:{port} open')
        else:
            print(f'> {host}:{port} close')


def curl_test(url):
    pass

# define host and port numbers to scan
HOST = '192.168.46.43'
PORTS = [22,80,8080,5432]
# test the ports
port_scan(HOST, PORTS)

HOST = 'google.co.kr'
PORTS = [80]
port_scan(HOST, PORTS)