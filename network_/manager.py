import argparse
import socket

class NetworkManager:
    def __init__(self, client_socket, buff_size):
        self.sock      = client_socket
        self.buff_size = buff_size
    
    def send_int(self, int_number):
        bytes_number = int_number.to_bytes(self.buff_size, 'big')
        self.sock.send(bytes_number)

    def recv_bytes_w_size(self):
        inbound_size_bytes = self.sock.recv(self.buff_size)
        inbound_size = int.from_bytes(inbound_size_bytes, 'big')
        inbound_msg  = b""
        while inbound_size > 0:
            chunk = self.sock.recv(self.buff_size)
            inbound_size -= len(chunk)
            inbound_msg  += chunk
        return inbound_msg  

    def recv(self):
        return pickle.loads(self.recv_bytes_w_size())

    def send_bytes_w_size(self, outbound_msg):
        outbound_size = len(outbound_msg)
        self.send_int(outbound_size)
        for chunk in range(0, outbound_size, self.buff_size):
            self.sock.send(outbound_msg[chunk:chunk+self.buff_size])
    
    def send(self, msg):
        self.send_bytes_w_size(pickle.dumps(msg))
 
    def close(self):
        self.sock.close()
