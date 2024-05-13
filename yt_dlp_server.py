import argparse
import socket
import threading

from os import urandom
 
from network_.manager import NetworkManager
from ytdlp.helper import process_query 

BUFF_SIZE = 16
OUTPUT_DIR = '/home/steganopus/Documents/TAoS/misc/20220814/server_client_kivy/kivy/media' 

def main(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    print(f'[*] Listening on {ip}:{port}')
    while True:
        sock, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}: {address[1]})')
        threading.Thread(target=YtDlpHandler.make_handler_and_run, args=(sock, BUFF_SIZE)).start()


class YtDlpHandler(NetworkManager):
    def run(self):
        try:
            # data = self.recv()
            data = self.recv()
            data = self.recv()
            filename = process_query(data['query'], data['add_video'], data['high_quality'], OUTPUT_DIR)
            self.send({'filename': filename})
            self.send({'filename': filename})
            # self.file_send(f'{OUTPUT_DIR}/{filename}')
            print(f'[*] Received: {data} of length {len(data)} and type {type(data)}')
        except Exception as e:
            print(e)

    @staticmethod
    def make_handler_and_run(sock, buff_size):
        handler = YtDlpHandler(sock, buff_size)
        handler.run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip',   type=str, required=True)
    parser.add_argument('--port', type=int, required=True)
    args = parser.parse_args()
    main(args.ip, args.port)

