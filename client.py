#!python3

import socket
import struct
import logging
import pickle
import sys

DEFAULT_MCAST_GRP = '224.1.1.1'
DEFAULT_MCAST_PORT = 5007
IS_ALL_GROUPS = True

MESSAGES = {
    'usage': '<client> [[-h <server>], [-p <port>], [-g <group>]]'
}

if '--help' in sys.argv or '-h' not in sys.argv:
    print('Usage: ' + MESSAGES['usage'])
    exit(1)

client_name = socket.gethostname()
client = socket.gethostbyname(client_name)
server_name = sys.argv[sys.argv.index('-h') + 1]
server = socket.gethostbyname(server_name)
port = DEFAULT_MCAST_PORT

# Verify if any option is in the arguments
if len(sys.argv) > 3:
    if '-p' in sys.argv:
        port = int(sys.argv[sys.argv.index('-p') + 1])
    if '-g' in sys.argv:
        grp = int(sys.argv[sys.argv.index('-g') + 1])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if IS_ALL_GROUPS:
    # on this port, receives ALL multicast groups
    sock.bind(('', port))
else:
    # on this port, listen ONLY to MCAST_GRP
    sock.bind((DEFAULT_MCAST_GRP, port))
mreq = struct.pack('4sl', socket.inet_aton(DEFAULT_MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive data until CTRL + C
try:
    while True:
        received = sock.recvfrom(4096)
        data = pickle.loads(received[0])

        # For debug purposes
        # positionStr = str(data['id']) + ' > ' + 'X: ' + str(data['X_pos']).rjust(4) + ' Y: ' + str(data['Y_pos']).rjust(4)
        # print(positionStr, end='')
        # print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\nFinalizando cliente...')
    exit(1)