#!python3

import socket
import pyautogui
import logging
import pickle
import sys

DEFAULT_MCAST_GRP = '224.1.1.1'
DEFAULT_MCAST_PORT = 5007
DEFAULT_MCAST_TTL = 2

MESSAGES = {
    'usage': '<server> [[-p <port>], [-t <ttl>], [-g <group>]]' 
}

if '--help' in sys.argv:
    print('Usage: ' + MESSAGES['usage'])
    exit(1)

host_name = socket.gethostname()
host = socket.gethostbyname(host_name)
port = DEFAULT_MCAST_PORT
ttl = DEFAULT_MCAST_TTL
grp = DEFAULT_MCAST_GRP

# Verify if any option is in the arguments
if len(sys.argv) > 1:
    if '-p' in sys.argv:
        port = int(sys.argv[sys.argv.index('-p') + 1])
    if '-t' in sys.argv:
        ttl = int(sys.argv[sys.argv.index('-t') + 1])
    if '-g' in sys.argv:
        grp = int(sys.argv[sys.argv.index('-g') + 1])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

# Send data until CTRL + C
try:
    counter = 0
    while True:
        # Cursor positions and window size data
        x, y = pyautogui.position()
        w, h = pyautogui.size()

        data = {
            'id'    : counter,
            'X_pos' : x,
            'Y_pos' : y,
            'width' : w,
            'height': h
        }

        # For debug purposes
        # positionStr = 'X: ' + str(data['X_pos']).rjust(4) + ' Y: ' + str(data['Y_pos']).rjust(4)
        # print(positionStr, end='')
        # print('\b' * len(positionStr), end='', flush=True)

        sock.sendto(pickle.dumps(data), (grp, port))
        counter += 1
except KeyboardInterrupt:
    print('\nFinalizando servidor...')
    exit(1)