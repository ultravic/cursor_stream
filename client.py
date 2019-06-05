#!python3

import socket
import struct
import logging
import pickle
import sys
import settings

# Library for graphics
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage.filters as filters

# Disable matplotlib logging debug
mpl_logger = logging.getLogger('matplotlib') 
mpl_logger.setLevel(logging.WARNING)

logging.basicConfig(filename = settings.LOGGING_FILE_CLIENT,
            filemode = 'w',
            format = settings.LOGGING_FORMAT, 
            level = settings.LOGGING_LEVEL, 
            datefmt = settings.LOGGING_DFT)
logger = logging.getLogger(__name__)

# Connection initialization function


def connection(HOST, PORT, GROUP):
    '''
    Create a socket of UDP/IP. The socket is set to multicast format.
    It's possible to set the TTL of the socket and to bind to a specific
    group or all groups.
    '''
    try:
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        logger.info('Socket created')
    except:
        logger.error('Error on socket creation')
        exit(0)

    if settings.IS_ALL_GROUPS:
        # on this port, receives ALL multicast groups
        sock.bind(('', PORT))
    else:
        # on this port, listen ONLY to MCAST_GRP
        sock.bind((GROUP, PORT))

    mreq = struct.pack('4sl', socket.inet_aton(GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    return sock

def plot(data, title, save_path):
    '''
    Creates a graphical visualization of the data. It's possible to send
    the graphic result to a file.
    '''
    plt.figure(figsize=(10,6), dpi=100)
    plt.imshow(data, cmap='hot')
    plt.xlabel("Width")
    plt.ylabel("Height")
    plt.title(title)

    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

def init(argv):
    if '--help' in argv or '-h' not in argv:
        print('Usage: ' + settings.MESSAGES['usage_client'])
        print('> Needed parameters :')
        for param in settings.MESSAGES['descr_client']['needed']:
            print('\t - ' + param)
        print('> Optional parameters:')
        for param in settings.MESSAGES['descr_client']['optional']:
            print('\t - ' + param)
        exit(0)

    # Verify if any option is in the arguments
    host = argv[argv.index('-h') + 1]
    if '-p' in argv:
        port = int(argv[argv.index('-p') + 1])
    else:
        port = settings.DEFAULT_MCAST_PORT
    if '-g' in argv:
        grp = int(argv[argv.index('-g') + 1])
    else:
        grp = settings.DEFAULT_MCAST_GRP

    try:
        sock = connection(host, port, grp) 
        logger.info('Socket connection succeeded')
    except:
        logger.error('Error on socket connection')
        exit(0)

    # Receive data until CTRL + C
    try:
        packets = []
        missing = []
        off_order = []
        packet_counter = 0
        scroll_counter = 0
        click_counter = 0
        click_vfy = False
        packet_vfy = 0

        # Wait for first packet
        received = sock.recvfrom(280)
        data = pickle.loads(received[0])

        logger.info("Firs packet received id:%d", data['id'])
        packet_vfy = data['id']

        # Print actions to debug
        logger.debug('Pointer moved to {0}'.format(data['mouse_position']))
        if data['mouse_pressed'] and not click_vfy:
            click_counter += 1
            click_vfy = True
            logger.debug('{0} at {1}'.format('Pressed', data['mouse_position']))
        elif not data['mouse_pressed'] and click_vfy:
            click_vfy = False
            logger.debug('{0} at {1}'.format('Released', data['mouse_position']))
        if data['mouse_scrolled'][0]:
            scroll_counter += 1
            logger.debug('Scrolled {0} at {1}'.format(data['mouse_scrolled'][1], data['mouse_position']))
        
        packets.append(data)
        packet_counter += 1

        while True:
            received = sock.recvfrom(280)
            data = pickle.loads(received[0])

            # Verify missing packets and out of order packets
            if data['id'] != packet_vfy + 1:
                missing.append(data)
                logger.critical("Missing packet id:%d", (packet_vfy + 1))
                packet_vfy = data['id']
            else:
                packet_vfy += 1

            if data['id'] < packet_vfy:
                off_order.append(data)
                logging.critical("Out of order packet id:%d", data['id'])

            # Print actions to debug
            logger.debug('Pointer moved to {0}'.format(data['mouse_position']))
            if data['mouse_pressed'] and not click_vfy:
                click_counter += 1
                click_vfy = True
                logger.debug('{0} at {1}'.format('Pressed', data['mouse_position']))
            elif not data['mouse_pressed'] and click_vfy:
                click_vfy = False
                logger.debug('{0} at {1}'.format('Released', data['mouse_position']))
            if data['mouse_scrolled'][0]:
                scroll_counter += 1
                logger.debug('Scrolled {0} at {1}'.format(data['mouse_scrolled'][1], data['mouse_position']))
            
            packets.append(data)
            packet_counter += 1
        click_vfy = False
    except KeyboardInterrupt:
        if packet_counter:
            logger.info('Last packet received id:%d', data['id'])
            logger.info('Number of packets received is %d', packet_counter)
            logger.info('Number of packets missing is %d', len(missing))
            logger.info('Number of packets out of order is %d', len(off_order))
            logger.info('Number of clicks received is %d', click_counter)
            logger.info('Number of scrolls received is %d', scroll_counter)

            # Create a base array
            grid = np.zeros(data['screen_size'][1] * data['screen_size'][0])
            grid = grid.reshape((data['screen_size'][1], data['screen_size'][0]))
            grid_pos = grid.copy()
            grid_scr = grid.copy()
            grid_prd = grid.copy()

            # Update pixels
            for packet in packets:
                grid_pos[packet['mouse_position'][1]][packet['mouse_position'][0]] += 1
                if packet['mouse_scrolled'][0]:
                    grid_scr[packet['mouse_position'][1]][packet['mouse_position'][0]] += 1
                if packet['mouse_pressed'] and not click_vfy:
                    click_vfy = True
                    grid_prd[packet['mouse_position'][1]][packet['mouse_position'][0]] += 10
                elif packet['mouse_pressed'] and click_vfy:
                    grid_prd[packet['mouse_position'][1]][packet['mouse_position'][0]] += 1
                elif not packet['mouse_pressed'] and click_vfy:
                    click_vfy = False

            # Add effect filter
            grid_pos = filters.gaussian_filter(grid_pos, sigma=10)
            grid_scr = filters.gaussian_filter(grid_scr, sigma=10)
            grid_prd = filters.gaussian_filter(grid_prd, sigma=10)
            
            # Plot the graphics to file or show
            if '-simage' in argv:
                plot(grid_pos, 'Cursor Heatmap', settings.SAVE_CURSOR)
                plot(grid_scr, 'Scroll Heatmap', settings.SAVE_SCROLL)
                plot(grid_prd, 'Click Heatmap', settings.SAVE_PRESS)
            else:
                plot(grid_pos, 'Cursor Heatmap', '')
                plot(grid_scr, 'Scroll Heatmap', '')
                plot(grid_prd, 'Click Heatmap', '')
        else:
            logger.info('No packets received')

        sock.close()
        logger.info('Socket closed')
        logger.info('Closing server')
        exit(1)

init(sys.argv)
