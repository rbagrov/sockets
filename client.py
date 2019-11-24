import os
import socket
import sys
import json
import argparse
from colorama import Fore, Style
from simplecrypt import encrypt

parser = argparse.ArgumentParser(description='Simple TCP socket client')
parser.add_argument('--message', dest='message', default=' ', help='Message to send')
parser.add_argument('--config', dest='cfg', default=None, help='Path to config file')
arguments = parser.parse_args()

BUFF_SIZE = 4096

if not arguments.cfg:
    print(f"{Fore.RED} Missing Config ! {Style.RESET_ALL}\n")
    sys.exit()

with open(arguments.cfg, 'r') as json_config:
    config = json.load(json_config)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((config['HOST'], config['PORT']))
        sock.sendall(bytes(encrypt(os.environ.get('SOCKET_SHARED_SECRET'), arguments.message)))
        received = sock.recv(4096).decode()

        print(f"{Fore.GREEN}Data: {Style.RESET_ALL}{received}")

except Exception:
    print(f"{Fore.RED} Bad config or unresponsive server!{Style.RESET_ALL}\n")
