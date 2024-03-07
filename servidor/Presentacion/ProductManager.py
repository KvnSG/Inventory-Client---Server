import json
from tkinter import messagebox

from Negocio.DatosCompartidos import DatosCompartidos
from Negocio.Producto import Producto
from Servidor.Cliente import Client
import tkinter as tk
import socket

class ProductManager():
    def __init__(self, root, Client):
        self.Client = Client
        self.root = root
        self.codigo_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.cantidad_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.descripcion_var = tk.StringVar()
        self.imagen_var = tk.StringVar()

    def agregar_producto(self):
        codigo = self.codigo_var.get()
        nombre = self.nombre_var.get()
        precio = self.precio_var.get()
        cantidad = self.cantidad_var.get()
        categoria = self.categoria_var.get()
        descripcion = self.descripcion_var.get()
        imagen = self.imagen_var.get()

        producto = {
            "codigo": codigo,
            "nombre": nombre,
            "precio": precio,
            "cantidad": cantidad,
            "categoria": categoria,
            "descripcion": descripcion,
            "imagen": imagen
        }



        # Verificar si el producto ya existe en la lista
        for registro in DatosCompartidos.registros:
            if registro["codigo"] == codigo:
                # Actualizar el producto existente
                registro.update({
                    "nombre": nombre,
                    "precio": precio,
                    "cantidad": cantidad,
                    "categoria": categoria,
                    "descripcion": descripcion,
                    "imagen": imagen
                })
                producto_actualizado = Producto(codigo, nombre, precio, cantidad, categoria, descripcion, imagen)
                return producto_actualizado.__dict__
                break
        else:
            # Si el producto no existe, agregar uno nuevo
            producto = Producto(codigo, nombre, precio, cantidad, categoria, descripcion, imagen)
            DatosCompartidos.registros.append(producto.__dict__)
            self.Client.send_data(json.dumps(producto.__dict__))
            return producto.__dict__


    def editar_producto(self):
        # Obtener el item seleccionado en la tabla
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Error", "Seleccione un producto para editar.")
            return

        # Obtener los valores del producto seleccionado
        item_id = seleccion[0]
        valores = self.tabla.item(item_id, 'values')

        # Llenar el formulario con los valores del producto seleccionado
        self.codigo_var.set(valores[0])
        self.nombre_var.set(valores[1])
        self.precio_var.set(valores[2])
        self.cantidad_var.set(valores[3])
        self.categoria_var.set(valores[4])
        self.descripcion_var.set(valores[5])
        self.imagen_var.set(valores[6])