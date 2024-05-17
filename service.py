import socket
import threading

from network_.manager import NetworkManager

SERVICE_IP   = "127.0.0.1"
SERVICE_PORT = 3002
BUFF_SIZE = 4096

def handle_ui(ui_sock):
    ui_nm = NetworkManager(ui_sock, BUFF_SIZE)
    request_data = ui_nm.recv()
    IP, PORT = request_data["IP"], request_data["PORT"]
    server = socket.socket()
    server.connect((str(IP), int(PORT)))
    server_nm = NetworkManager(server, BUFF_SIZE)
    server_nm.send({"query": request_data["query"],
                    "add_video": request_data["add_video"],
                    "high_quality": request_data["high_quality"]})
    file_meta = server_nm.recv()
    private_filename = f"{request_data['data_dir']}/{file_meta['filename']}"
    server_nm.file_receive(private_filename)
    server_nm.close()
    ui_nm.send("finished")
    ui_nm.send("Done")
    ui_nm.close()

if __name__ == '__main__':
    service_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    service_sock.bind((SERVICE_IP, SERVICE_PORT))
    service_sock.listen(5)
    while True:
        ui_sock, _ = service_sock.accept()
        threading.Thread(target=handle_ui, args=(ui_sock, )).start()


