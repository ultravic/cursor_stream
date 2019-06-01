#!python3

import socket
import struct
import logging
import pickle
import sys
from Tkinter import *

# Default variables
DEFAULT_MCAST_GRP = '224.1.1.1'
DEFAULT_MCAST_PORT = 5007
IS_ALL_GROUPS = True
MESSAGES = {
    'usage': '<client> [[-h <server>], [-p <port>], [-g <group>]]'
}

# Connection initialization function


def connection(HOST, PORT, GROUP):
    client_name = socket.gethostname()
    client = socket.gethostbyname(client_name)
    server = socket.gethostbyname(HOST)

    try:
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except:
        print("Erro ao criar socket")
        exit(0)

    if IS_ALL_GROUPS:
        # on this port, receives ALL multicast groups
        sock.bind(('', PORT))
    else:
        # on this port, listen ONLY to MCAST_GRP
        sock.bind((GROUP, PORT))
    mreq = struct.pack('4sl', socket.inet_aton(GROUP), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    return sock


def init(argv):
    if '--help' in argv or '-h' not in argv:
        print('Usage: ' + MESSAGES['usage'])
        exit(0)

    # Verify if any option is in the arguments
    host = argv[argv.index('-h') + 1]
    if '-p' in argv:
        port = int(argv[argv.index('-p') + 1])
    else:
        port = DEFAULT_MCAST_PORT
    if '-g' in argv:
        grp = int(argv[argv.index('-g') + 1])
    else:
        grp = DEFAULT_MCAST_GRP

    sock = connection(host, port, grp)

    master = Tk()

    w = Canvas(master, width=200, height=100)
    w.pack()

    w.create_line(0, 0, 200, 100)
    w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

    # Receive data until CTRL + C
    try:
        while True:
            received = sock.recvfrom(4096)
            data = pickle.loads(received[0])

            # For debug purposes
            positionStr = str(data['id']) + ' > ' + 'X: ' + str(data['mouse_position']
                                                                [0]).rjust(4) + ' Y: ' + str(data['mouse_position'][1]).rjust(4)
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
    except KeyboardInterrupt:
        print('\nFinalizando cliente...')
        exit(1)


init(sys.argv)
