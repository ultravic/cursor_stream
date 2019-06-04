# This is a configuration file
import logging

# Default
DEFAULT_MCAST_GRP = '224.1.1.1'
DEFAULT_MCAST_PORT = 5007
DEFAULT_MCAST_TTL = 2
IS_ALL_GROUPS = True
MESSAGES = {
    'usage_server': '<server> [[-p <port>], [-t <ttl>], [-g <group>]]',
    'usage_client': '<client> -h <server_name> [[-p <port>], [-g <group>], [-simage]]',
    'descr_server': [
                        '<port>: port where socket will be created',
                        '<ttl>: time to live of the packets'
    ],
    'descr_client': {
                    'needed': [
                        '<server_name>: name of the server that the socket \
                        will be receiving data'
                    ],
                    'optional': [
                        '<port>: port where socket will be created',
                        'simage: save the graphics to images folder'
                    ]
    }
}

# Save files
SAVE_CURSOR = 'images/cheat.jpg'
SAVE_SCROLL = 'images/sheat.jpg'
SAVE_PRESS = 'images/pheat.jpg'
IMAGE_FORMAT = 'jpg'

# Logging
LOGGING_LEVEL = logging.INFO
LOGGING_FILE_SERVER = 'logs/server.log'
LOGGING_FILE_CLIENT = 'logs/client.log'
LOGGING_FORMAT = '%(asctime)s [%(levelname)s]: %(message)s'
LOGGING_DFT = '%m-%d-%Y %I:%M:%S'