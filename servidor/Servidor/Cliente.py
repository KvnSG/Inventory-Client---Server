from socket import socket

import socket
class Client:
    def __init__(self, host=" ", port=65432):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.host, self.port))
        except ConnectionRefusedError:
            print("No se pudo conectar al servidor.")
            exit()

    def send_data(self, data):
        self.client.sendall(data.encode("utf-8"))