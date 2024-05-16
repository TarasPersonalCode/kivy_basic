import socket
import threading

from network_.manager import NetworkManager

SERVICE_IP   = "127.0.0.1"
SERVICE_PORT = 3002
BUFF_SIZE = 4096

def handle_ui(ui_sock):
    ui_nm = NetworkManager(ui_sock, BUFF_SIZE)
    test_data = ui_nm.recv()
    test_data["test"] = "lololo"
    ui_nm.send(test_data)
    ui_nm.close()

if __name__ == '__main__':
    service_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    service_sock.bind((SERVICE_IP, SERVICE_PORT))
    service_sock.listen(5)
    while True:
        ui_sock, _ = service_sock.accept()
        threading.Thread(target=handle_ui, args=(ui_sock, )).start()


