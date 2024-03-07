import threading

from Servidor.Cliente import Client
from Presentacion.UIManager import UIManager
from Presentacion.DetallesProducto import DetalleProducto
from Presentacion.ProductManager import ProductManager
import tkinter as tk
from tkinter import ttk
from Servidor.Server import Server


if __name__ == "__main__":
    #servidor_ip = '192.168.100.49'  # Cambia esto por la IP del servidor al que te quieres conectar
    #servidor_puerto = 65432    # Cambia esto por el puerto del servidor

    #app = UIManager()
    #ventana_secundaria = DetalleProducto(app, "Tienda XYZ")
    #app.agregar_observer(ventana_secundaria)
    #app.mainloop()

    server_thread = threading.Thread(target=Server().accept_connections)
    server_thread.start()

    # Iniciar la interfaz de usuario
    app = UIManager()
    app.mainloop()