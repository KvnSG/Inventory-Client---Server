import socket
import threading
import json

from Negocio.DatosCompartidos import DatosCompartidos
from Presentacion.UIManager import UIManager


class Server:
    def __init__(self, host="", port=65432):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.server.bind((self.host, self.port))
        self.server.listen()

    def accept_connections(self):
        print("El servidor está escuchando en", self.host, ":", self.port)
        while True:
            client, address = self.server.accept()
            print(f"Conexión establecida desde {address}")
            self.clients.append(client)
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        while True:
            try:
                data = client.recv(1024)
                if data:
                    # Aquí se manejan los datos recibidos
                    self.broadcast(data)
                    self.process_data(data)
                    print(data)
            except ConnectionResetError:
                self.clients.remove(client)
                client.close()
                break

    def broadcast(self, data):
        for client in self.clients:
            try:
                client.sendall(data)
            except:
                self.clients.remove(client)

    def process_data(self, data):
        # Decodificar los datos JSON
        decoded_data = json.loads(data)

        # Actualizar o agregar los datos en DatosCompartidos.registros
        codigo = decoded_data.get("codigo")
        if codigo:
            # Verifica si ya existe un registro con el mismo código
            for registro in DatosCompartidos.registros:
                if registro["codigo"] == codigo:
                    # Actualiza el registro existente
                    registro.update(decoded_data)
                    break
            else:
                # Agrega un nuevo registro
                DatosCompartidos.registros.append(decoded_data)

        # Obtener la instancia de UIManager
        ui_manager = UIManager.getInstance()

        # Notificar a los observadores y actualizar la interfaz de usuario
        ui_manager.notificar_observers(decoded_data)
        ui_manager.actualizar_tabla()
