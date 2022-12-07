from tkinter import ttk
from tkinter import *
import time

class Product:

    def __init__(self, window):
        self.wind = window
        self.wind.title('TEST CLICK')
        frame= LabelFrame(self.wind, text="")
        ttk.Button(frame,text="Guardar Producto")

if __name__ == '__main__':#evaluamos si nos encontramos en el main
    window = Tk()
    window.geometry("1000x660+0+0")
    application = Product (window)
    window.mainloop()