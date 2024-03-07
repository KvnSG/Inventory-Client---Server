import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod


class Observable(ABC):
    @abstractmethod
    def agregar_observer(self, observer):
        pass

    @abstractmethod
    def quitar_observer(self, observer):
        pass

    @abstractmethod
    def notificar_observers(self, datos):
        pass