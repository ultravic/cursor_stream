#!python3

import socket
import logging
import pickle
import sys
import time
# Cursor librarys
import pyautogui
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller

# Default variables
DEFAULT_MCAST_GRP = '224.1.1.1'
DEFAULT_MCAST_PORT = 5007
DEFAULT_MCAST_TTL = 2
MESSAGES = {
    'usage': '<server> [[-p <port>], [-t <ttl>], [-g <group>]]' 
}

logging.basicConfig(format = '%(asctime)s [%(levelname)s]: %(message)s', level = logging.INFO, datefmt = '%m-%d-%Y %I:%M:%S')

# Packet structure
data = {
    'id'    : 0,
    'mouse_position' : (0,0),
    'mouse_pressed' : False,
    'mouse_scrolled' : False,
    'screen_size' : (0, 0),
}

# Connection initialization function
def connection(PORT, GROUP, TTL):
    host_name = socket.gethostname()
    host = socket.gethostbyname(host_name)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
        logging.info('Socket created')
    except:
        logging.error('Error on socket creation')
        exit(0)

    return sock

def on_move(x, y):
    data['mouse_position'] = (x,y)
    logging.debug('Pointer moved to {0}'.format((x, y)))

def on_click(x, y, button, pressed):
    data['mouse_pressed'] = pressed
    logging.debug('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))

def on_scroll(x, y, dx, dy):
    data['mouse_scrolled'] = True
    logging.debug('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up', (x, y)))

def init(argv):
    if '--help' in argv:
        print('Usage: ' + MESSAGES['usage'])
        exit(0)

    # Verify if any option is in the arguments
    if '-p' in argv:
        port = int(argv[argv.index('-p') + 1])
    else:
        port = DEFAULT_MCAST_PORT
    if '-t' in argv:
        ttl = int(argv[argv.index('-t') + 1])
    else:
        ttl = DEFAULT_MCAST_TTL
    if '-g' in argv:
        grp = int(argv[argv.index('-g') + 1])
    else:
        grp = DEFAULT_MCAST_GRP

    try:
        sock = connection(port, grp, ttl)
        logging.info('Socket connection succeeded')
    except:
        logging.error('Error on socket connection')
        exit(0)

    # Send data until CTRL + C
    try:
        counter = 0
        # Collect events until released
        listener = mouse.Listener(
                on_move=on_move, 
                on_click=on_click, 
                on_scroll=on_scroll)
        try:
            listener.start()
            logging.info('Mouse listener started')
        except:
            loggin.error('Mouse listener start failed')
            exit(0)
        

        screen_w, screen_h = pyautogui.size()
        try:
            data['id'] = counter
            data['screen_size'] = (screen_w, screen_h)
            time.sleep(0.0001)
            sock.sendto(pickle.dumps(data), (grp, port))
            data['id'] = counter
            data['mouse_scrolled'] = False
            counter += 1
            logging.info('First packet sent succefuly')
        except:
            logging.error('Sending packet failed')
            exit(0)

        while True:
            time.sleep(0.0001)
            sock.sendto(pickle.dumps(data), (grp, port))
            data['id'] = counter
            data['mouse_scrolled'] = False
            counter += 1
    except KeyboardInterrupt:
        logging.info('Last packet sent id:%d', data['id'])
        listener.stop()
        logging.info('Mouse listener closed')
        logging.info('Closing server')
        exit(1)

init(sys.argv)