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
        threading.Thread(target=YtDlpHandler.make_handler_and_run, args=(sock, BUFF_SIZE)).start()


class YtDlpHandler:
    def __init__(self, client_socket, buff_size):
        self.sock      = client_socket
        self.buff_size = buff_size

    def run(self):
        data = self.sock.recv(self.buff_size)
        while len(data) > 0:
            print(f'[*] Received: {data} of length {len(data)} and type {type(data)}')
            data = self.sock.recv(self.buff_size)
    
    def send_int(self, int_number):
        bytes_number = int_number.to_bytes(self.buff_size, 'big')
        self.sock.send(bytes_number)

    def recv_string_w_size(self):
        inbound_size_bytes = self.sock.recv(self.buff_size)
        inbound_size = int.from_bytes(inbound_size_bytes, 'big')
        inbound_msg  = b""
        while inbound_size > 0:
            chunk = self.sock.recv(self.buff_size)
            inbound_size -= len(chunk)
            inbound_msg  += chunk
        return inbound_msg.decode('utf-8')

    def send_string_w_size(self, string):
        outbound_msg = string.encode('utf-8')
        outbound_size = len(outbound_msg)
        self.send_int(outbound_size)
        for chunk in range(0, outbound_size, self.buff_size):
            self.sock.send(outbound_msg[chunk:chunk+self.buff_size])
        
        
    
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

