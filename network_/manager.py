import os
import pickle
import socket
import time

from network_.file_receiver import NetworkFileReceiver

class NetworkManager:
    def __init__(self, client_socket, buff_size):
        self.sock      = client_socket
        self.buff_size = buff_size
    
    def send_int(self, int_number):
        bytes_number = int_number.to_bytes(self.buff_size, 'big')
        self.sock.send(bytes_number)

    def recv_bytes_w_size(self):
        inbound_size_bytes = self.receive_bytes_of_size(self.buff_size)
        inbound_size = int.from_bytes(inbound_size_bytes, 'big')
        return self.receive_bytes_of_size(inbound_size)

    def receive_bytes_of_size(self, inbound_size):
        inbound_msg  = b""
        while inbound_size > 0:
            chunk = self.sock.recv(min(self.buff_size, inbound_size))
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

    def file_send(self, filename):
        filesize = os.path.getsize(filename)
        sentfrac = 0
        self.send(filesize)
        with open(filename, 'rb') as f:
            l = f.read(self.buff_size)
            start_time = time.time()
            while l:
                self.sock.send(l)
                l = f.read(self.buff_size)
                sentfrac += self.buff_size / filesize
                elapsed   = time.time() - start_time
                print(f'Progress:      {round(sentfrac, 2)}; '
                      f's; elapsed:    {round(elapsed)}'
                      f's; remaining:  {round(elapsed / (sentfrac + 0.1) * (1 - sentfrac), 1)}')

    # def file_receive(self, filename):
    #     NetworkFileReceiver(self, filename, 10).receive_all()

