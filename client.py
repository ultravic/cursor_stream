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

logging.basicConfig(filename=settings.LOGGING_FILE_CLIENT,
                    filemode='w',
                    format=settings.LOGGING_FORMAT,
                    level=settings.LOGGING_LEVEL,
                    datefmt=settings.LOGGING_DFT)
logger = logging.getLogger(__name__)

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


def verifyMissingPackets(seems_missing, missing_cnt, data):
    # print(*seems_missing)
    a = False
    # Verify if "missing" packets are realy missed (farther than an window size from the last packet)
    for miss in seems_missing:
        if(data['id'] > miss + settings.DEFAULT_WINDOW_SIZE):
            logger.critical("Missing packet id:%d", miss)
            missing_cnt += 1
            del seems_missing[seems_missing.index(miss)]
            a = True
    if(a):
        logger.critical("Packet triggered missing :%d", data['id'])
    
    return missing_cnt


def plot(data, title, save_path):
    '''
    Creates a graphical visualization of the data. It's possible to send
    the graphic result to a file.
    '''
    plt.figure(figsize=(10, 6), dpi=100)
    plt.imshow(data, cmap='hot')
    plt.xlabel("Width")
    plt.ylabel("Height")
    plt.title(title)

    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

def helper(argv):
    '''
    Prints the instructions of the client.
    '''
    print('Usage: ' + settings.MESSAGES['usage_client'])
    print('> Needed parameters :')
    for param in settings.MESSAGES['descr_client']['needed']:
        print('\t - ' + param)
    print('> Optional parameters:')
    for param in settings.MESSAGES['descr_client']['optional']:
        print('\t - ' + param)
    exit(0)


def init(argv):
    if '--help' in argv or '-h' not in argv:
        helper(argv)

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
        missing_cnt = 0
        off_order = 0
        packet_counter = 0
        scroll_counter = 0
        click_counter = 0
        click_vfy = False
        greatest_pack = 0

        # Wait for first packet
        received = sock.recvfrom(280)
        data = pickle.loads(received[0])

        logger.info("First packet received id:%d", data['id'])
        greatest_pack = data['id']

        # Print actions to debug
        logger.debug('Pointer moved to {0}'.format(data['mouse_position']))
        if data['mouse_pressed'] and not click_vfy:
            click_counter += 1
            click_vfy = True
            logger.debug('{0} at {1}'.format(
                'Pressed', data['mouse_position']))
        elif not data['mouse_pressed'] and click_vfy:
            click_vfy = False
            logger.debug('{0} at {1}'.format(
                'Released', data['mouse_position']))
        if data['mouse_scrolled'][0]:
            scroll_counter += 1
            logger.debug('Scrolled {0} at {1}'.format(
                data['mouse_scrolled'][1], data['mouse_position']))

        packets.append(data)
        packet_counter += 1
        while True:
            received = sock.recvfrom(280)
            data = pickle.loads(received[0])

            missing_cnt = verifyMissingPackets(missing, missing_cnt, data)

            # Verify if the packet is ahead of time
            if data['id'] > greatest_pack + 1:
                logger.critical(
                    "Packet ahead of time id:%d -- curr: %d", data['id'], greatest_pack)
                for miss in range(greatest_pack + 1, data['id']):
                    missing.append(miss)
                # del packets[packets.index(data)]
                greatest_pack = data['id']
            else:
                # Verify if is out of order
                if data['id'] in missing:
                    idx = missing.index(data['id'])
                    logger.critical("Packet out of order id:%d",
                                    missing[idx]['id'])
                    off_order += 1
                    del missing[idx]
                else:
                    if ((np.random.randint(0, 100) % 100) < 10):
                        # Simulate a 1 % packet loss rate
                        pass
                        # printf("Pretending to have dropped a packet!\n");}
                    else:
                        #  handle the incoming packet as usual
                        logger.critical("Packet in order:%d", data['id'])
                        greatest_pack = data['id']

            # Print actions to debug
            logger.debug('Pointer moved to {0}'.format(data['mouse_position']))
            if data['mouse_pressed'] and not click_vfy:
                click_counter += 1
                click_vfy = True
                logger.debug('{0} at {1}'.format(
                    'Pressed', data['mouse_position']))
            elif not data['mouse_pressed'] and click_vfy:
                click_vfy = False
                logger.debug('{0} at {1}'.format(
                    'Released', data['mouse_position']))
            if data['mouse_scrolled'][0]:
                scroll_counter += 1
                logger.debug('Scrolled {0} at {1}'.format(
                    data['mouse_scrolled'][1], data['mouse_position']))

            packets.append(data)
            packet_counter += 1
            # print(missing_cnt)

        missing_cnt = verifyMissingPackets(missing, missing_cnt, data)
        
        click_vfy = False
    except KeyboardInterrupt:
        if packet_counter:
            logger.info('Last packet received id:%d', data['id'])
            logger.info('Number of packets received is %d', packet_counter)
            logger.info('Number of packets missing is %d', missing_cnt)
            logger.info('Number of packets out of order is %d', off_order)
            logger.info('Number of clicks received is %d', click_counter)
            logger.info('Number of scrolls received is %d', scroll_counter)

            # Create a base array
            grid = np.zeros(data['screen_size'][1] * data['screen_size'][0])
            grid = grid.reshape(
                (data['screen_size'][1], data['screen_size'][0]))
            grid_pos = grid.copy()
            grid_scr = grid.copy()
            grid_prd = grid.copy()

            # Update pixels
            for packet in packets:
                grid_pos[packet['mouse_position'][1]
                         ][packet['mouse_position'][0]] += 10
                if packet['mouse_scrolled'][0]:
                    grid_scr[packet['mouse_position'][1]
                             ][packet['mouse_position'][0]] += 10
                if packet['mouse_pressed'] and not click_vfy:
                    click_vfy = True
                    grid_prd[packet['mouse_position'][1]
                             ][packet['mouse_position'][0]] += 10
                elif packet['mouse_pressed'] and click_vfy:
                    grid_prd[packet['mouse_position'][1]
                             ][packet['mouse_position'][0]] += 1
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
        logger.info('Closing client')
        exit(1)


init(sys.argv)
