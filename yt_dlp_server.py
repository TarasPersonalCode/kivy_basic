import argparse
import socket
import threading

from os import urandom
 
BUFF_SIZE = 16

def main(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    print(f'[*] Listening on {ip}:{port}')
    while True:
        sock, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}: {address[1]})')
        threading.Thread(target=YtDlpHandler.make_handler_and_run, args=(sock,)).start()


class YtDlpHandler:
    def __init__(self, client_socket):
        self.sock = client_socket

    def run(self):
        data = urandom(BUFF_SIZE) 
        while len(data) == BUFF_SIZE:
            data = self.sock.recv(BUFF_SIZE)
            print(f'[*] Received: {data} of length {len(data)}')
        
    @staticmethod
    def make_handler_and_run(sock):
        handler = YtDlpHandler(sock)
        handler.run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip',   type=str, required=True)
    parser.add_argument('--port', type=int, required=True)
    args = parser.parse_args()
    main(args.ip, args.port)

