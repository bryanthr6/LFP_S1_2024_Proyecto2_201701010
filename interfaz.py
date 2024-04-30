import tkinter as tk
from tkinter import filedialog

#variable raiz representa la ventana principal
raiz = tk.Tk()


def hola():
    print('Hola')



#Definir el título de la ventana
titulo_ventana = 'LFP A+ - Bryant Herrera Rubio - Proyecto 2'
raiz.title(titulo_ventana)

#Cambiar la imagen en la esquina superior izquierda de la ventana
raiz.iconbitmap('FIUSAC.ico')

#Aquí es para definier el tamaño de la ventana y centrarla
#definir tamaño de la ventana
ancho_ventana= 900
alto_ventana= 600
#Obtener información de las dimensiones de la pantalla de donde se está ejecutando el programa
ancho_pantalla = raiz.winfo_screenwidth()
alto_pantalla = raiz.winfo_screenheight()
#calcular las coordenadas en posición X y Y de la pantalla
x_pos = (ancho_pantalla - ancho_ventana) // 2
y_pos = ((alto_pantalla - alto_ventana) // 2 ) - 40
#Centrar la ventana
raiz.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

#Color de fondo de la ventana
raiz.configure(bg='lightsteelblue4')

#Evitar que la ventana se pueda redimensionar
raiz.resizable(False ,False)


#Fuente personalizada para botones
fuente_personalizada = ('Comic Sans MS', 10)


#Método mainloop() inicia el bucle de eventos, permite que la ventana esté abierta y responda a las interacciones del usuario
#La instrucción mainloop tiene que ir siempre al final
raiz.mainloop()