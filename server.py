#!python3

import socket
import pyautogui
import logging
import pickle
import sys
import time

from pynput import mouse, keyboard
from pynput.mouse import Button, Controller

# Default variables
DEFAULT_MCAST_GRP = '224.1.1.1'
DEFAULT_MCAST_PORT = 5007
DEFAULT_MCAST_TTL = 2
MESSAGES = {
    'usage': '<server> [[-p <port>], [-t <ttl>], [-g <group>]]' 
}


global mouse_pressed, mouse_position, mouse_scrolled

# Connection initialization function
def connection(PORT, GROUP, TTL):
    host_name = socket.gethostname()
    host = socket.gethostbyname(host_name)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
    except:
        print("Erro ao criar socket!")
        exit(0)

    return sock


# def logger(x,y):
#     # For debug purposes
#     positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
#     print(positionStr, end='')
#     print('\b' * len(positionStr), end='', flush=True)


def on_move(x, y):
    global mouse_position 
    mouse_position = (x,y)
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_click(x, y, button, pressed):
    global mouse_pressed 
    mouse_pressed = pressed
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))

def on_scroll(x, y, dx, dy):
    global mouse_scrolled 
    mouse_scrolled = dy 
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))
    print('dy {0}'.format(dy))

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

    sock = connection(port, grp, ttl)
    global mouse_pressed
    global mouse_position
    global mouse_scrolled 
    mouse_pressed = False
    mouse_position = (0,0)
    mouse_scrolled = False

    # Send data until CTRL + C
    try:
        counter = 0
        # # # Collect events until released
        listener = mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll)
        listener.start()
        
        screen_w, screen_h = pyautogui.size()

        while True:
            time.sleep(0.01)
            data = {
                'id'    : counter,
                'mouse_position' : mouse_position,
                'mouse_pressed' : mouse_pressed,
                'mouse_scrolled' : mouse_scrolled,
                'screen_size' : (screen_w, screen_h),
            }
            sock.sendto(pickle.dumps(data), (grp, port))
            counter += 1
    except KeyboardInterrupt:
        print('\nFinalizando servidor...')
        listener.stop()
        exit(1)

init(sys.argv)