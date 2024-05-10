import socket
import threading
import time

from os import urandom

IP = '0.0.0.0'
PORT = 9998

BUFF_SIZE = 16

input_file = './sample.txt'

def main():
    client = socket.socket()
    client.connect((IP, PORT))
    file = open(input_file, 'rb')
    byte = urandom(BUFF_SIZE)
    while len(byte) == BUFF_SIZE:
        byte = file.read(BUFF_SIZE)
        client.send(byte)

if __name__ == '__main__':
    main()

