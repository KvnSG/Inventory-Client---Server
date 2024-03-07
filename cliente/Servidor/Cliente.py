import json
import threading
from socket import socket
from Negocio.DatosCompartidos import DatosCompartidos


import socket
class Client:
    def __init__(self, host="", port=65432):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.host, self.port))
        except ConnectionRefusedError:
            print("No se pudo conectar al servidor.")
            exit()

        threading.Thread(target=self.receive_updates).start()

    def send_data(self, data):
        self.client.sendall(data.encode("utf-8"))

    def receive_updates(self):
        while True:
            try:
                data = self.client.recv(1024)
                if data:
                    # Procesa los datos recibidos y actualiza la interfaz de usuario
                    self.process_server_data(data)
            except ConnectionResetError:
                print("Conexión perdida con el servidor.")
                break

    def process_server_data(self, data):
        from Presentacion.UIManager import UIManager
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