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
        client, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}: {address[1]})')
        client_handler = threading.Thread (target = handle_client, args = (client,))
        client_handler.start()

def handle_client(client_socket):
    with client_socket as sock:
        data = urandom(BUFF_SIZE) 
        while len(data) == BUFF_SIZE:
            data = sock.recv(BUFF_SIZE)
            print(f'[*] Received: {data} of length {len(data)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip',   type=str, required=True)
    parser.add_argument('--port', type=int, required=True)
    args = parser.parse_args()
    main(args.ip, args.port)

