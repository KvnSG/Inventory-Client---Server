import json
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from urllib.request import urlopen
from io import BytesIO
from abc import ABC, abstractmethod
from Negocio.Observable import Observable
from Negocio.Producto import Producto
from Negocio.DatosCompartidos import DatosCompartidos
from Presentacion.ProductManager import ProductManager
from Servidor.Cliente import Client
class UIManager(tk.Tk, Observable):
    _instance = None


    def __init__(self):

        if not UIManager._instance:
            UIManager._instance = self
            super().__init__()
            Observable.__init__(self)
            client = Client()
            self.title("Ventana Principal")

            self.configure(bg="#f0f0f0")  # Fondo gris claro

            # Crear el contenedor de paneles

            self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
            self.paned_window.pack(expand=True, fill=tk.BOTH)

            # Panel izquierdo (formulario)
            self.product_manager = ProductManager(self, client)

            formulario_frame = ttk.Frame(self.paned_window, padding=10)
            formulario_frame.grid(row=0, column=0, sticky="nsew")

            etiquetas = ["Código:", "Nombre:", "Precio:", "Cantidad:", "Categoría:", "Descripción:",
                         "URL de la Imagen:"]
            campos_var = [self.product_manager.codigo_var, self.product_manager.nombre_var, self.product_manager.precio_var,
                          self.product_manager.cantidad_var, self.product_manager.categoria_var, self.product_manager.descripcion_var, self.product_manager.imagen_var]

            for i, etiqueta in enumerate(etiquetas):
                tk.Label(formulario_frame, text=etiqueta, bg="#f0f0f0").grid(row=i, column=0, pady=5, padx=5,
                                                                             sticky="e")
                tk.Entry(formulario_frame, textvariable=campos_var[i], width=30).grid(row=i, column=1, pady=5, padx=5,
                                                                                      sticky="w")

            tk.Button(formulario_frame, text="Agregar Producto", command=lambda: self.notificar_observers(self.product_manager.agregar_producto()), bg="#4caf50",
                      fg="white").grid(row=7, column=0, columnspan=2, pady=10)

            # Nuevo botón para editar producto
            tk.Button(formulario_frame, text="Editar Producto", command=lambda: self.notificar_observers(self.product_manager.editar_producto()), bg="#2196F3",
                      fg="white").grid(row=8, column=0, columnspan=2, pady=10)

            # Panel derecho (tabla)
            tabla_frame = ttk.Frame(self.paned_window, padding=10)
            tabla_frame.grid(row=0, column=1, sticky="nsew")

            # Tabla
            self.tabla = ttk.Treeview(tabla_frame, columns=(
                "Código", "Nombre", "Precio", "Cantidad", "Categoría", "Descripción", "Imagen"))
            self.tabla.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

            # Configuración de encabezados de la tabla
            self.tabla.heading("#0", text="ID")
            encabezados = ["Código", "Nombre", "Precio", "Cantidad", "Categoría", "Descripción", "Imagen"]
            for i, encabezado in enumerate(encabezados):
                self.tabla.heading(encabezado, text=encabezado)

            # Ajuste de columnas
            for col in encabezados:
                self.tabla.column(col, anchor="center")
                self.tabla.column("#0", anchor="center", width=0)  # Oculta la primera columna (ID)

            self.observers = []  # Inicializa la lista de observers

            # Agregar los paneles al contenedor de paneles
            self.paned_window.add(formulario_frame)
            self.paned_window.add(tabla_frame)

    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def agregar_observer(self, observer):
        self.observers.append(observer)
        self.actualizar_tabla()

    def quitar_observer(self, observer):
        self.observers.remove(observer)
        self.actualizar_tabla()

    def notificar_observers(self, datos):
        for observer in self.observers:
            observer.actualizar(datos)
        self.actualizar_tabla()

    def actualizar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        for registro in DatosCompartidos.registros:
            self.tabla.insert("", tk.END, values=(
                registro["codigo"], registro["nombre"], registro["precio"],
                registro["cantidad"], registro["categoria"], registro["descripcion"], registro["imagen"]
            ))
