import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def actualizar(self, datos):
        pass