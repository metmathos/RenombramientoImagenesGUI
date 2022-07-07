'''
APLICACION PARA RENOMBRAMIENTO DE ARCHIVOS DE IMAGENES
Por Matias Herrera

Fecha inicio: 25/06/2022

Esta aplicacion solo sirve para archivos .jpg o .jpeg
Tiene un correccion para algunos archivos personales comenzados con
la cadena 'sam',los cuales tenian un desfase de 672 dias en su
fecha de captura.
Alguna/s caracteristica/s a cambiar a futuro:
* Borrado de listbox 'listaObtenidos' y text 'textoRuta' a traves de boton 'botonObtener' si
  estos ya se encontraban llenos
* Chequear archivos que tengan metadatos borrados
* Poner messagebox de "Esperar a que se renombren los archivos", dado que a veces se tarda en renombrar por la cantidad de ARCHIVOS

Fecha de terminacion de 1ra revision: 04/07/2022
Version 1.0
'''

import tkinter
from tkinter import filedialog
import os
import exifread
from datetime import datetime, timedelta

# Con el metodo Tk() se inicializa una ventana
ventana=tkinter.Tk()

# Se agrega un titulo a la ventana
ventana.title("Renombramiento de nombres de imagenes")

# Con la funcion 'geometry' se dimensiona la ventana.
# El parametro es "<ancho>x<alto>"
ventana.geometry("800x620")

# Se define la funcion para llenar el listbox 'listaObtenidos' y el text 'textoRuta',
# con los archivos del directorio elegido y la ruta del mismo, respectivamente
def imprimirArchivos(ruta, lista, texto):
    #Solo se procede si existe la ruta
    if(ruta):
        archivos = os.listdir(ruta)
        # Se agregan los archivos en el listbox
        for index,elem in enumerate(archivos):
            lista.insert(index, archivos[index])
        # Se pasa la configuracion del text a normal, para poder ingresar la cadena
        texto.config(state='normal')
        texto.insert(1.0,ruta)
        # Se vuelve la configuracion a deshabilitado, para que el text no sea modificable
        texto.config(state='disabled')

# Se define la funcion para abrir el cuadro de seleccion de directorio y luego se llama
# a la funcion 'imprimirArchivos'
def abrirArchivos(list, texto):
    archivo = filedialog.askdirectory(title="Abrir", initialdir="C:/")
    imprimirArchivos(archivo,list, texto)

# Se crea la funcion que contiene la logica de renombramiento de archivos JPG y que tambien tiene
# el llenado del listbox 'listaRenombrados'
def renombrarArchivos(texto, listaO):
    # Se obtiene la ruta a partir del text 'rutaObtenida'
    # Se selecciona desde el primer caracter '1.0' hasta el ultimo sin el salto de linea 'end-1c'
    rutaObtenida = texto.get("1.0", "end-1c")

    # Se crea una lista vacia para anexar los archivos .jpg o .jpeg
    archivos=[]

    # Se usa la lista tieneSAM para almacenar una lista de booleanos que correspondan a la lista de rutas que contengan archivos que comiencen con 'sam',
    # que son imagenes con fecha de captura incorrecta por un desfasaje de 672 dias
    tieneSAM=[]

    # Se crea una lista vacia para anexar los archivos renombrados para ser pasados al listbox 'listaRenombrados'
    obtenidos=[]

    # Se listan los archivos de la ruta pasada como argumento del text 'textoRuta':
    # Se chequea que la cadena no este vacia
    if(rutaObtenida!=''):
            lista = os.listdir(rutaObtenida)

            for archivo in lista:
                # Se pasan las cadenas a minuscula
                archivo = archivo.lower()

                if(archivo.endswith(".jpg") or archivo.endswith(".jpeg")):
                    # Chequea si hay que modificar fecha respecto a como comienza el archivos
                    if(archivo.startswith("sam")):
                        tieneSAM.append(True)
                    else:
                        tieneSAM.append(False)
                    # Se pasa la ruta entera (full path) de los archivos - Se usa la cadena "\\" para escapar la barra \:
                    ruta=str(rutaObtenida)+"\\"+str(archivo)
                    # Si la ruta exista, se almacena en la lista 'archivos':
                    if (os.path.exists(ruta)):
                        archivos.append(ruta)

            # Se concatenan las listas de tieneSAM y la lista de rutas
            lista_archivos = list(zip(tieneSAM,archivos))

            # Se envia un messagebox con error si no se ha encontrado ningun archivo .jpg o .jpeg
            if(len(archivos)==0):
                tkinter.messagebox.showinfo("Advertencia","El directorio no contiene archivos JPG o JPEG")

            for file in lista_archivos:

                with open(file[1], 'rb') as imagen:
                    # Obtiene valores exif de imagen
                    valores_exif = exifread.process_file(imagen)

                    # Imprimir valores de la imagen
                    for tag in valores_exif.keys():

                        if(str(tag)=="EXIF DateTimeOriginal"):
                            if(file[0]):
                                # Se toma el valor correspondiente al tag 'EXIF DateTimeOriginal' y
                                # se lo transforma en un objeto datetime
                                fecha=datetime.strptime(str(valores_exif[tag]),"%Y:%m:%d %H:%M:%S")
                                # Al objeto datetime se le agregan 672 dias
                                mod=fecha+timedelta(days=672)
                                # Se asigna al valor correspondiente al tag 'EXIF DateTimeOriginal'
                                # el valor datetime modificado y corregido
                                valores_exif[tag] = str(mod).replace('-','')
                            nombre_nuevo=str(valores_exif[tag])
                            # En las proximas dos lineas se arregla el nombre del archivo
                            # para que coincida con el formato de cadena elegido
                            nombre_nuevo = nombre_nuevo.replace(':','')
                            nombre_nuevo = nombre_nuevo.replace(' ','_')
                            obtenidos.append(nombre_nuevo)

                if(nombre_nuevo.endswith(".jpg")):
                    os.rename(file[1],str(rutaObtenida)+"\\"+str(nombre_nuevo)+".jpg")
                else:
                    os.rename(file[1],str(rutaObtenida)+"\\"+str(nombre_nuevo)+".jpeg")

            for index,elem in enumerate(obtenidos):
                listaO.insert(index, obtenidos[index])
    # Se envia un messagebox si la cadena sacada del text 'textoRuta' esta vacia
    else:
        tkinter.messagebox.showinfo("Advertencia","No ha seleccionado ninguna ruta")

# Funcion para cerrar la aplicacion
def close_window():
    ventana.destroy()

# A continuacion se declaran los widgets que van ubicados en la ventana principal 'ventana'
#
#
# Se utilizo el metodo .place() antes que el metodo .pack(), dado que este ultimo apilaba los
# widgets, dejando un aspecto mas desordenado.
# El metodo place() tiene la sgte sintaxis:
#     <widget>.place(x=<punto de inicio en el eje X>, y=<punto de inicio en el eje Y>, width=<ancho del widget>, height=<alto del widget>)
#
# Con el metodo pack() se ubican los objetos dentro de la ventana sin ubicacion exacta(si no tiene parametro)
#     Con el parametro pack(side=tkinter.BOTTOM), la etiqueta se ubica al fondo de la ventana
#     Con el parametro pack(side=tkinter.TOP), la etiqueta se ubica al tope de la ventana
# El metodo pack es mejor usado con el metodo .grid()

#Etiqueta de advertencia de uso de la aplicacion
label0 = tkinter.Label(ventana, text="NOTA: Esta aplicacion solo funciona con archivos .JPG o .JPEG", bg="yellow", font=("Verdana",12))
label0.place(x=10, y=5, width=780, height=20)

#Etiqueta para listbox 'listaObtenidos'
label1 = tkinter.Label(ventana,text="Archivos a renombrarse (si aplican):",bg="grey")
label1.place(x=10, y=45, width=240, height=20)

#Etiqueta para lista 'listaRenombrados'
label2 = tkinter.Label(ventana,text="Archivos renombrados:",bg="grey")
label2.place(x=490, y=45, width=240, height=20)

# Etiqueta para text 'rutaObtenida'
label3 = tkinter.Label(ventana, text="Ubicacion abierta:")
label3.place(x=10, y=540, width=100, height=20)


listaObtenidos = tkinter.Listbox(ventana)
listaObtenidos.place(x=10, y=70, width=300, height=400)

listaRenombrados = tkinter.Listbox(ventana)
listaRenombrados.place(x=490, y=70, width=300, height=400)


textoRuta = tkinter.Text(ventana, bg="#cad0cd", state='disabled')
textoRuta.place(x=120, y=540, width=650, height=20)

# Se configura un botton, que como comando tiene a la funcion 'abrirArchivos'
# a traves del parametro 'command'. La funcion va sin parentesis, porque se
# se pusiera parentesis, se ejectaria la funcion cuando se abra la ventana
# si se necesita pasar una funcion con parametro, se debe usar una lambda
botonObtener = tkinter.Button(ventana, text="Abrir Ubicacion", command=lambda: abrirArchivos(listaObtenidos, textoRuta))
botonObtener.place(x=10, y=490, width=100, height=40)

# Se configura boton para poner en funcionamientos la logica de renombramiento y el llenado de la listbox 'listaRenombrados' a
# traves de la funcion 'renombrarArchivos'
botonRenombrar = tkinter.Button(ventana, text="Renombrar archivos", command=lambda: renombrarArchivos(textoRuta, listaRenombrados))
botonRenombrar.place(x=330, y=200, width=140, height=50)

# Se configura boton de cierre de la aplicacion
botonCierre = tkinter.Button(text = "Cerrar", command = close_window)
botonCierre.place(x=680,y=570,width=100,height=40)

# Al parecer, PhotoImage solo funciona con archivos .png
# Este tipo de metodo no redimensiona las imagenes, las recorta
imagen=tkinter.PhotoImage(file="flecha.png")
lbl_img = tkinter.Label(ventana, image=imagen)
lbl_img.place(x=330, y=250, width=140, height=140)

# mainloop debe ser para hacer un loop de refresco de frames y registro de eventos
ventana.mainloop()
