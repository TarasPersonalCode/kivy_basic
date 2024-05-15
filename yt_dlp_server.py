import argparse
import socket
import threading

from os import urandom
 
from network_.manager import NetworkManager

from ytdlp.helper import process_query 

def main(ip, port, buff_size, output_dir):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    print(f'[*] Listening on {ip}:{port}')
    while True:
        sock, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}: {address[1]}')
        threading.Thread(target=YtDlpHandler.make_handler_and_run, args=(sock, buff_size, output_dir)).start()


class YtDlpHandler(NetworkManager):
    def __init__(self, sock, buff_size, output_dir):
        super().__init__(sock, buff_size)
        self.output_dir = output_dir

    def run(self):
        try:
            data = self.recv()
            print(f'[*] Received: {data} of length {len(data)} and type {type(data)}')
            filename = process_query(data['query'], data['add_video'], data['high_quality'], self.output_dir)
            self.send({'filename': filename})
            self.file_send(f'{OUTPUT_DIR}/{filename}')
        except Exception as e:
            print(e)

    @staticmethod
    def make_handler_and_run(sock, buff_size):
        handler = YtDlpHandler(sock, buff_size)
        handler.run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip',         type=str, required=True)
    parser.add_argument('--port',       type=int, required=True)
    parser.add_argument('--buff-size',  type=int, required=True)
    parser.add_argument('--output-dir', type=str, required=True)
    args = parser.parse_args()
    main(args.ip, args.port, args.buff_size, args.output_dir)

