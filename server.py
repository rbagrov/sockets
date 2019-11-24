import os
import sys
import socketserver
from colorama import Fore, Back, Style
import json
import argparse
from simplecrypt import encrypt, decrypt
from graphene import ObjectType, String, Schema
import psutil


class Query(ObjectType):
    cpu = String()

    def resolve_cpu(root, info):
        percent = psutil.cpu_percent()
        return f'{percent}%'


class Server(socketserver.BaseRequestHandler):

    def setup(self):
        self.schema = Schema(query=Query)

    def handle(self):
        self.data = self.request.recv(4096).strip()
        decrypted_data = decrypt(os.environ.get('SOCKET_SHARED_SECRET'), self.data)

        decoded_data = decrypted_data.decode()

        print(f"{Fore.GREEN}Client FROM {Style.RESET_ALL}<{Fore.YELLOW}{self.client_address[0]}{Style.RESET_ALL}>>>> {Back.WHITE}{Fore.BLACK}{decoded_data}{Style.RESET_ALL}\n")

        percent = self.schema.execute(decoded_data).data[decoded_data.strip('{}')]
        self.request.sendall(bytes(encrypt(os.environ.get('SOCKET_SHARED_SECRET'), percent.encode())))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Simple TCP socket server')
    parser.add_argument('--config', dest='cfg', default=None, help='Path to config file')
    arguments = parser.parse_args()

    if not arguments.cfg:
        print(f"{Fore.RED} Missing Config ! {Style.RESET_ALL}\n")
        sys.exit()

    with open(arguments.cfg, 'r') as json_config:
        config = json.load(json_config)

    try:
        with socketserver.TCPServer((config['HOST'], config['PORT']), Server) as server:
            server.serve_forever()
    except Exception:
        print(f"{Fore.RED} Bad config!{Style.RESET_ALL}\n")
