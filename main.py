import sqlite3
from tkinter import ttk
from tkinter import *
import time

class Product:
    db_name ='D:\\Escritorio\\UCASAL\\2022\\LENGUAJES 1\\TRABAJOS PRACTICOS\\EXPOSICION\\database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('MOBILE DATA')

        #CREAMOS LA BARRA DEL MENU
        barraMenu=Menu(self.wind)

        #CRAMOS LOS MENUS
        mnuArchivo=Menu(barraMenu)
        mnuEdicion=Menu(barraMenu)
        mnuPersonalizacion=Menu(barraMenu)

        #CREMOS LAS OPCIONES DE CADA MENU DESPLEGABLE
        mnuArchivo.add_command(label="Abrir")
        mnuArchivo.add_command(label="Nuevo")
        mnuArchivo.add_command(label="Guardar")
        mnuArchivo.add_separator()
        mnuArchivo.add_command(label="Actualizar Tablas" ,command=self.obtener_products)
        mnuArchivo.add_separator()
        mnuArchivo.add_command(label='EXIT',command=window.destroy)

        mnuEdicion.add_command(label='Tema')

        mnuPersonalizacion.add_command(label='Tema Rojo',command=self.tema_rojo)
        mnuPersonalizacion.add_command(label='Tema Blanco',command=self.tema_blanco)
        mnuPersonalizacion.add_command(label='Tema Dark',command=self.tema_dark)
        mnuPersonalizacion.add_command(label='Tema Azul', command=self.tema_azul)


        #AGREGAR MENUS A LA BARRA
        barraMenu.add_cascade(label="Archivo",menu=mnuArchivo)
        barraMenu.add_cascade(label='Edicion',menu=mnuEdicion)
        barraMenu.add_cascade(label="Personalizacion",menu=mnuPersonalizacion)
    
        #AGREGAR LA BARRA DE MENU A LA VENTANA
        window.config(menu=barraMenu,bg='red')

        #creamos un contenedor
        frame= LabelFrame(self.wind, text="Resgistrar un nuevo producto")
        frame.grid(row=0, column=0 , columnspan=3 , pady=20)
        Label(frame, text="Nombre: ").grid(row=1, column=0)
        self.name=Entry(frame)
        self.name.focus()
        self.name.grid(row=1,column=1)
        Label(frame, text='Precio: ').grid(row=2,column=0)
        self.price=Entry(frame)
        self.price.grid(row=2,column=1)

        #addprod
        ttk.Button(frame,text="Guardar Producto",command= self.add_prod).grid(row=3,columnspan=2,sticky=W+E)

        #mensaje exito o no
        self.message=Label(text='', fg='red')
        self.message.grid(row=3,column=0,columnspan=2,sticky=W+E)


        self.tree=ttk.Treeview(height=19, columns=2)
        self.tree.grid(row=4,column=0,columnspan=2)
        self.tree.heading('#0', text='Nombre', anchor=CENTER)
        self.tree.heading('#1', text='Precio', anchor=CENTER)

        #botones
        ttk.Button(text='Borrar item' , command=self.borrarItem).grid(row=5,column=0,sticky=(W+E))
        ttk.Button(text='Editar item',command=self.editarItem).grid(row=5,column=1,sticky=(W+E))

        #rellenando filas
        self.obtener_products()

        #obtenemos la hora actual y le aplicamos un tema
        self.obtener_hora()

        #RELOJ (LIBRERIA TIME)
        self.texto_hora=Label(text="",bg='black',fg='white',font=('calibri',38,'bold'))
        self.texto_hora.grid(row=6,columnspan=2)
        self.hora_actualizada()

    #METODO PARA OBTENER LA HORA
    def obtener_hora(self):
        hora_actual= time.strftime('%H:%M:%S')
        #tema diurno
        if hora_actual>=('07:00:00') and hora_actual <=('19:00:00'):
            self.wind['bg']='red'
        #tema nocturno
        else:       
            self.wind['bg']='blue'

    #METODO PARA ACTUALIZAR CONSTANTEMENTE LA HORA
    def hora_actualizada(self):
        hora=time.strftime('%H:%M:%S')
        self.texto_hora['text']=hora
        self.texto_hora.after(1000,self.hora_actualizada)
        #self.texto_hora.after(1000,self.obtener_products)

    #PERSONALIZACIONES (MENU)
    def tema_rojo(self):
        self.wind['bg']='red'
    def tema_blanco(self):
        self.wind['bg']='white'
    def tema_dark(self):
        self.wind['bg']='black'
    def tema_azul(self):
        self.wind['bg']='blue'

    #ENVIO DE ORDENES Y PARAMETROS A LA BASE DE DATOS
    def correr_datos(self,query,parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query,parameters)
            conn.commit()
        return result
    
    #OBTENCION DE DATOS DE LA BASE DE DATOS
    def obtener_products(self):
        print('a')
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query='SELECT * FROM products ORDER BY nombre DESC'
        db_filas = self.correr_datos(query)
        for filas in db_filas:
            self.tree.insert('',0,text=filas[1],values=filas[2])

    #VALIDACION DE FORMULARIO
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    #AGREGAMOS EL PRODUCTO A LA BASE DE DATOS
    def add_prod(self):
        if self.validation():
            #se se verifica la validacion agregamos el producto a la base de datos
            query = 'INSERT INTO products VALUES(NULL,?,?)'
            parameters = (self.name.get(),self.price.get())
            self.correr_datos(query,parameters)
            self.message['text']='Producto {} agregado Exitosamente'.format(self.name.get())
            self.name.delete(0,END)
            self.price.delete(0,END)
        else:
            #mostramos un mensaje si no se verifica la validacion
            self.message['text']='Nombre y precio son requeridos'
        self.obtener_products()

    #METODO PARA BORRAR EL PRODUCTO DE LA BASE DE DATOS
    def borrarItem(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Porfavor selecciona un item'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM products WHERE nombre = ?'
        self.correr_datos(query, (name, ))
        self.message['text'] = 'Item {} borrado satisfactoriamente'.format(name)
        self.obtener_products()

    #METODO PARA EDITAR EL ITEM
    def editarItem(self):
        self.message['text'] = " "
        try:
            self.tree.item(self.tree.selection())['text'][0]#si se encuentra selecconado sigue el codigo
        except IndexError as e:#si no se selecciona nada muestra mensaje error y no retorna nada y se para la ejecucion de esta funcion(es como un break)
            self.message['text'] = 'Porfavor selecciona un Item'
            return
        self.message['text'] = ''
        name_anterior = self.tree.item(self.tree.selection())['text']
        precio_anterior=self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()#cremos una ventana superpuesta
        self.edit_wind.geometry('250x130+50+50')
        self.edit_wind.title = 'Editar Producto'

        #nombre anterior
        Label(self.edit_wind, text='Nombre anterior').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=name_anterior), state='readonly').grid(row=0 ,column=2)
        #nuevo nombre
        Label(self.edit_wind , text='Nuevo Nombre').grid(row=1,column=1)
        nuevo_nombre= Entry(self.edit_wind)
        nuevo_nombre.grid(row=1,column=2)

        #precio anterior
        Label(self.edit_wind , text='Precio Anterior').grid(row=2,column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind,value=precio_anterior) , state='readonly').grid(row=2,column=2)

        #precio nuevo
        Label(self.edit_wind, text='Nuevo Precio').grid(row=3,column=1)
        nuevo_precio=Entry(self.edit_wind)
        nuevo_precio.grid(row=3,column=2)

        #boton para actualizar los datos
        Button(self.edit_wind, text='Actualizar data' , command=lambda:self.edit_data(nuevo_nombre.get(),name_anterior,nuevo_precio.get(),precio_anterior)).grid(row=4,columnspan=3)

    #metodo para actualizar la tabla en la base de datos enviando parametros nuevos
    def edit_data(self , nuevo_nombre, nombre , nuevo_precio , precio):
        query= 'UPDATE products SET nombre = ?,precio = ? WHERE nombre = ? AND precio = ?'
        parameters = (nuevo_nombre,nuevo_precio,nombre,precio)
        self.correr_datos(query,parameters)
        self.edit_wind.destroy()
        self.message['text']='El Item {} ha sido actualizado correctamente.'.format(nombre)
        self.obtener_products()#actualizamos la tabla en pantalla


if __name__ == '__main__':#evaluamos si nos encontramos en el main
    window = Tk()
    window.geometry("400x660+0+0")
    application = Product (window)
    window.mainloop()