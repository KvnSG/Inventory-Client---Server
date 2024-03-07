import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from abc import ABC, abstractmethod
from Negocio.Observer import Observer
import socket
import threading
import json

class DetalleProducto(tk.Toplevel, Observer):
    def __init__(self, ventana_principal, nombre):
        tk.Toplevel.__init__(self, ventana_principal)
        Observer.__init__(self)

        self.ventana_principal = ventana_principal  # Almacenar la referencia de la ventana principal
        self.title(f"Tienda en Línea - {nombre}")

        # Marco principal
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Encabezado
        tk.Label(main_frame, text="Productos Disponibles", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=10)

        # Lista de productos
        self.lista_productos = ttk.Treeview(main_frame, columns=(
        "Código", "Nombre", "Precio", "Categoría", "Descripción", "Imagen"))
        self.lista_productos.pack(padx=20, pady=10)

        # Configuración de encabezados de la lista de productos
        encabezados = ["Código", "Nombre", "Precio", "Categoría", "Descripción", "Imagen"]
        for i, encabezado in enumerate(encabezados):
            self.lista_productos.heading(encabezado, text=encabezado)

        # Ajuste de columnas
        for col in encabezados:
            self.lista_productos.column(col, anchor="center")

        # Botones para dejar y volver a escuchar
        tk.Button(main_frame, text="Offline", command=self.dejar_de_escuchar, bg="#d32f2f", fg="white").pack(pady=10)
        tk.Button(main_frame, text="Online", command=self.volver_a_escuchar, bg="#4caf50", fg="white").pack(pady=10)

        self.escuchando = True

    def dejar_de_escuchar(self):
        if self.escuchando:
            self.ventana_principal.quitar_observer(self)
            self.escuchando = False

    def volver_a_escuchar(self):
        if not self.escuchando:
            self.ventana_principal.agregar_observer(self)
            self.escuchando = True

    def actualizar(self, datos):
        codigo = datos.get("codigo", "")
        nombre = datos.get("nombre", "")
        precio = datos.get("precio", "")
        categoria = datos.get("categoria", "")
        descripcion = datos.get("descripcion", "")
        imagen = datos.get("imagen", "")

        # Buscar el item correspondiente en la lista
        encontrado = False
        for item_id in self.lista_productos.get_children():
            valores = self.lista_productos.item(item_id, 'values')
            if valores and valores[0] == codigo:
                # Actualizar los valores del producto existente
                self.lista_productos.item(item_id, values=(codigo, nombre, precio, categoria, descripcion, imagen))
                encontrado = True
                break

        # Si no se encuentra el producto, agregar uno nuevo
        if not encontrado:
            self.lista_productos.insert("", tk.END, values=(codigo, nombre, precio, categoria, descripcion, imagen))
