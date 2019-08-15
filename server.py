import sys
import socketserver
from colorama import Fore, Back, Style
import json
import argparse

class Server(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(4096).strip()
        print(f"{Fore.GREEN}Client FROM {Style.RESET_ALL}<{Fore.YELLOW}{self.client_address[0]}{Style.RESET_ALL}>>>> {Back.WHITE}{Fore.BLACK}{self.data.decode('utf-8')}{Style.RESET_ALL}\n")
        self.request.sendall(self.data)

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
    except Exception as e:
        print(f"{Fore.RED} Bad config!{Style.RESET_ALL}\n")
