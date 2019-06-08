#!python3

import socket
import logging
import pickle
import sys
import time
import settings

# Cursor librarys
import pyautogui
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller

logging.basicConfig(filename=settings.LOGGING_FILE_SERVER,
                    filemode='w',
                    format=settings.LOGGING_FORMAT,
                    level=settings.LOGGING_LEVEL,
                    datefmt=settings.LOGGING_DFT)
logger = logging.getLogger(__name__)

# Packet structure
data = {
    'id': 1,
    'mouse_position': (0, 0),
    'mouse_pressed': False,
    'mouse_scrolled': (False, ''),
    'screen_size': (0, 0),
}

def connection(TTL):
    '''
    Create a socket of UDP/IP. The socket is set to multicast format.
    It's possible to set the TTL of the socket.
    '''
    try:
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
        logger.info('Socket created')
    except:
        logger.error('Error on socket creation')
        exit(0)

    return sock

def on_move(x, y):
    ''' 
    On event, this function get the position (x,y) from
    the cursor. The position is assign to data packet.
    '''
    data['mouse_position'] = (x, y)
    logger.debug('Pointer moved to {0}'.format((x, y)))

def on_click(x, y, button, pressed):
    ''' 
    On event, this function get the press and release of the left
    mouse button. The action is assign to data packet.
    '''
    data['mouse_pressed'] = pressed
    logger.debug('{0} at {1}'.format(
        'Pressed' if pressed else 'Released', (x, y)))

def on_scroll(x, y, dx, dy):
    ''' 
    On event, this function get the scroll direction of the
    mouse button. The action is assign to data packet.
    '''
    data['mouse_scrolled'] = (True, 'down' if dy < 0 else 'up')
    logger.debug('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up', (x, y)))

def helper(argv):
    '''
    Prints the instructions of the server.
    '''
    print('Usage: ' + settings.MESSAGES['usage_server'])
    print('> Optional parameters:')
    for param in settings.MESSAGES['descr_server']:
        print('\t - ' + param)
    exit(0)

def init(argv):
    if '--help' in argv:
        helper(argv)        

    # Verify if any option is in the arguments
    if '-p' in argv:
        port = int(argv[argv.index('-p') + 1])
    else:
        port = settings.DEFAULT_MCAST_PORT
    if '-t' in argv:
        ttl = int(argv[argv.index('-t') + 1])
    else:
        ttl = settings.DEFAULT_MCAST_TTL
    if '-g' in argv:
        grp = int(argv[argv.index('-g') + 1])
    else:
        grp = settings.DEFAULT_MCAST_GRP
    if '-i' in argv:
        inter = float(argv[argv.index('-i') + 1])
    else:
        inter = settings.DEFAULT_TIME

    # Connection initialization function
    sock = connection(ttl)

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
            logger.info('Mouse listener started')
        except:
            logging.error('Mouse listener start failed')
            exit(0)

        # Define packets with data from the listener events and send through socket
        screen_w, screen_h = pyautogui.size()
        try:
            data['id'] = counter
            data['screen_size'] = (screen_w, screen_h)
            time.sleep(inter)
            sock.sendto(pickle.dumps(data), (grp, port))

            data['mouse_scrolled'] = (False, '')
            counter += 1
            logger.info('First packet sent succefuly')
        except:
            logger.error('Sending packet failed')
            exit(0)

        while True:
            time.sleep(inter)
            data['id'] = counter
            sock.sendto(pickle.dumps(data), (grp, port))

            data['mouse_scrolled'] = (False, '')
            counter += 1
    except KeyboardInterrupt:
        logger.info('Last packet sent id:%d', data['id'])
        listener.stop()
        logger.info('Mouse listener closed')
        sock.close()
        logger.info('Socket closed')
        logger.info('Closing server')
        exit(1)

init(sys.argv)
