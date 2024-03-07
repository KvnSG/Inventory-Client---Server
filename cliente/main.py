import threading

from Cliente import Client
from Presentacion.UIManager import UIManager
from Presentacion.DetallesProducto import DetalleProducto
from Presentacion.ProductManager import ProductManager
import tkinter as tk
from tkinter import ttk
from Servidor.Server import Server


if __name__ == "__main__":
    servidor_ip = ''  # Cambia esto por la IP del servidor al que te quieres conectar
    servidor_puerto = 65432    # Cambia esto por el puerto del servidor

    app = UIManager()
    ventana_secundaria = DetalleProducto(app, "Tienda XYZ - CLIENTE")
    app.agregar_observer(ventana_secundaria)
    app.mainloop()
