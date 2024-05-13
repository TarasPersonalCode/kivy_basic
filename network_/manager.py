import os
import pickle
import socket
import time

# from kivy import Logger

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
        print(f"[NetworkManager.recv_bytes_w_size]: {inbound_size=}")
        inbound_msg  = b""
        while inbound_size > 0:
            chunk = self.sock.recv(min(self.buff_size, inbound_size))
            inbound_size -= len(chunk)
            inbound_msg  += chunk
        print(f"[NetworkManager.recv_bytes_w_size]: {inbound_msg=}")
        return inbound_msg  

    def recv(self):
        return pickle.loads(self.recv_bytes_w_size())

    def send_bytes_w_size(self, outbound_msg):
        print(f"[NetworkManager.send_bytes_w_size]: {outbound_msg=}")
        outbound_size = len(outbound_msg)
        print(f"[NetworkManager.send_bytes_w_size]: {outbound_size=}")
        self.send_int(outbound_size)
        for chunk in range(0, outbound_size, self.buff_size):
            self.sock.send(outbound_msg[chunk:chunk+self.buff_size])
    
    def send(self, msg):
        self.send_bytes_w_size(pickle.dumps(msg))
 
    def close(self):
        self.sock.close()

    def file_send(self, filename):
        # from kivy import Logger
        print(f"{filename=}")
        filesize = os.path.getsize(filename)
        print(f"{filesize=}")
        self.send(filesize)
        with open(filename, 'rb') as f:
            l = f.read(self.buff_size)
            start_time = time.time()
            idx = 0
            while l:
                self.sock.send(l)
                l = f.read(self.buff_size)
                print(f'Progress:   {round(100 * idx * self.buff_size/ filesize, 2)}; '
                      f's; elapsed:    {round(time.time() - start_time)}'
                      f's; remaining: {round((time.time() - start_time) / (idx * self.buff_size / filesize + 0.0001) * (1 - idx * self.buff_size / 4096), 1)}')
                idx += 1

    def file_receive(self, filename):
        from kivy import Logger
        Logger.info(f"{filename=}")
        filesize = self.recv()
        Logger.info(f"{filesize=}")
        while filesize > 0:
            with open(filename, 'wb') as f:
                chunk = self.sock.recv(self.buff_size)
                f.write(chunk)
                filesize -= len(chunk)
                Logger.info(f'{filesize=}; {len(chunk)=}')
