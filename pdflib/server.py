import argparse
import os
import socket
import threading

from network_.manager import NetworkManager

from pdflib.helper import process_query 

def main(ip, port, buff_size, output_dir):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    print(f'[*] Listening on {ip}:{port}')
    while True:
        sock, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}: {address[1]}')
        threading.Thread(target=handle_client, args=(sock, buff_size, output_dir)).start()


def handle_client(sock, buff_size, output_dir):
    nm = NetworkManager(sock, buff_size)
    try:
        data = nm.recv()
        print(f'[*] Received: {data} of length {len(data)} and type {type(data)}')
        filename = process_query(data['query'], data['add_video'], data['high_quality'], output_dir)
        nm.send({'filename': filename, 'filesize': os.path.getsize(f'{output_dir}/{filename}')})
        nm.file_send(f'{output_dir}/{filename}')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip',         type=str, required=True)
    parser.add_argument('--port',       type=int, required=True)
    parser.add_argument('--buff-size',  type=int, required=True)
    parser.add_argument('--output-dir', type=str, required=True)
    args = parser.parse_args()
    main(args.ip, args.port, args.buff_size, args.output_dir)

