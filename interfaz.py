import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
from analizador import tokenize_input, tokens, error_messages

# Variable raíz representa la ventana principal
raiz = tk.Tk()

# Función de prueba
def hola():
    print('Hola')

# Función de Nuevo
def nuevo():
    if txt_entrada.get(1.0, "end-1c") != "":
        guardar_cambios = messagebox.askyesnocancel("Guardar cambios", "¿Desea guardar los cambios antes de limpiar el editor?")
        if guardar_cambios:
            guardar()
        elif guardar_cambios is None:  # Si el usuario cancela, no limpiamos el editor
            return
    txt_entrada.delete(1.0, "end")
    archivo_actual.set("")

# Función de Guardar
def guardar():
    if archivo_actual.get():  # Si hay un archivo actual, guardar sobre él
        with open(archivo_actual.get(), "w") as f:
            f.write(txt_entrada.get(1.0, "end-1c"))
    else:
        guardar_como()  # Si no hay archivo actual, llamar a la función guardar_como

# Función de Abrir
def abrir():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        with open(archivo, "r") as f:
            contenido = f.read()
            txt_entrada.delete(1.0, "end")
            txt_entrada.insert(1.0, contenido)
        archivo_actual.set(archivo)

# Función de Guardar Como
def guardar_como():
    archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        with open(archivo, "w") as f:
            f.write(txt_entrada.get(1.0, "end-1c"))
        archivo_actual.set(archivo)
        

def generar_reporte_tokens():
    # Generar el contenido HTML del reporte de tokens
    contenido_tokens_html = "<html>\n<head>\n<title>Reporte de Tokens</title>\n</head>\n<body>\n"
    
    # Agregar la sección de tokens al contenido HTML
    contenido_tokens_html += "<h1>Reporte de Tokens</h1>\n"
    if tokens:
        contenido_tokens_html += "<table border='1'>\n<tr><th>Token</th><th>Lexema</th><th>Línea</th><th>Columna</th></tr>\n"
        for token in tokens:
            contenido_tokens_html += f"<tr><td>{token.value}</td><td>{token.value}</td><td>{token.line}</td><td>{token.col}</td></tr>\n"
        contenido_tokens_html += "</table>\n"
    else:
        contenido_tokens_html += "<p>No se encontraron tokens.</p>\n"
    
    # Cerrar el contenido HTML
    contenido_tokens_html += "</body>\n</html>"
    
    # Escribir el contenido HTML en un archivo para el reporte de tokens
    with open("ReporteTokens.html", "w") as archivo_tokens:
        archivo_tokens.write(contenido_tokens_html)
    
    # Notificar al usuario que se ha generado el reporte de tokens
    print("Se ha generado el reporte de tokens en el archivo 'ReporteTokens.html'")


# Función para generar el reporte de errores en HTML
def generar_reporte_errores():
    # Generar el contenido HTML del reporte de errores
    contenido_errores_html = "<html>\n<head>\n<title>Reporte de Errores</title>\n</head>\n<body>\n"
    
    # Agregar la sección de errores al contenido HTML
    contenido_errores_html += "<h1>Reporte de Errores</h1>\n"
    if error_messages:
        contenido_errores_html += "<table border='1'>\n<tr><th>Carácter</th><th>Línea</th><th>Columna</th><th>Tipo de Error</th></tr>\n"
        for error, error_type in error_messages:
            parts = error.split()
            char = parts[-6]
            line = parts[-3]
            column = parts[-1]
            contenido_errores_html += f"<tr><td>{char}</td><td>{line}</td><td>{column}</td><td>{error_type}</td></tr>\n"
        contenido_errores_html += "</table>\n"
    else:
        contenido_errores_html += "<p>No se encontraron errores.</p>\n"
    
    # Cerrar el contenido HTML
    contenido_errores_html += "</body>\n</html>"
    
    # Escribir el contenido HTML en un archivo para el reporte de errores
    with open("ReporteErrores.html", "w") as archivo_errores:
        archivo_errores.write(contenido_errores_html)
    
    # Notificar al usuario que se ha generado el reporte de errores
    print("Se ha generado el reporte de errores en el archivo 'ReporteErrores.html'")


# Modificar la función ejecutar_analisis para que llame a las funciones adecuadas
def ejecutar_analisis():
    # Obtener el texto del cuadro de texto
    contenido = txt_entrada.get("1.0", "end-1c")
    
    # Tokenizar el contenido
    tokenize_input(contenido)
    
    # Generar los reportes de tokens y errores
    generar_reporte_tokens()
    generar_reporte_errores()


# Agrega un archivo actual para rastrear el archivo abierto
archivo_actual = tk.StringVar()
archivo_actual.set("")  # Inicialmente no hay archivo abierto

# Crear un widget Menu
menu_bar = tk.Menu(raiz)

# Crear el menú Archivo y agregarle opciones
menu_archivo = tk.Menu(menu_bar, tearoff=0)
menu_archivo.add_command(label="Nuevo", command=nuevo)
menu_archivo.add_command(label="Abrir", command=abrir)
menu_archivo.add_command(label="Guardar", command=guardar)
menu_archivo.add_command(label="Guardar Como", command=guardar_como)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=raiz.quit)

# Crear el menú Análisis y agregarle opciones
menu_analisis = tk.Menu(menu_bar, tearoff=0)
menu_analisis.add_command(label="Ejecutar análisis", command=ejecutar_analisis)

# Crear el menú Tokens y agregarle opciones
menu_tokens = tk.Menu(menu_bar, tearoff=0)
menu_tokens.add_command(label="Mostrar tokens", command=lambda: messagebox.showinfo("Reporte de Tokens", "Se generó la lista de tokens en el archivo 'ReporteTokens.html'."))



# Crear el menú Errores y agregarle opciones
menu_errores = tk.Menu(menu_bar, tearoff=0)
menu_errores.add_command(label="Mostrar errores", command=lambda: messagebox.showinfo("Reporte de Errores", "Se generó la lista de errores en el archivo 'ReporteErrores.html'."))


# Agregar los menús al menú principal
menu_bar.add_cascade(label="Archivo", menu=menu_archivo)
menu_bar.add_cascade(label="Análisis", menu=menu_analisis)
menu_bar.add_cascade(label="Tokens", menu=menu_tokens)
menu_bar.add_cascade(label="Errores", menu=menu_errores)

# Configurar la ventana para que use el menú
raiz.config(menu=menu_bar)

# Crear un Scrollbar vertical
scrollbar_entrada_vertical = tk.Scrollbar(raiz)
scrollbar_entrada_vertical.grid(row=1, column=1, padx=5, pady=5, sticky='ns')

# Fuente personalizada
fuente_personalizada = ('Comic Sans MS', 10)

# Etiquetas para identificar cuadro de texto "Texto de entrada"
etiqueta_izquierda = tk.Label(raiz, text="Texto de Entrada:", bg='lightsteelblue4', fg='white', font=fuente_personalizada)
etiqueta_izquierda.grid(row=0, column=0, padx=5, pady=5, sticky='w')
etiqueta_izquierda.place(x=20, y=65)

# Cuadro de texto para el texto de entrada
txt_entrada= tk.Text(raiz, width=106, height=27, wrap="none", yscrollcommand=scrollbar_entrada_vertical.set)
txt_entrada.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
txt_entrada.place(x=20, y=90)

# Configurar barras de desplazamiento para el cuadro de texto
scrollbar_entrada_vertical.config(command=txt_entrada.yview)

# Cambiar la posición de las barras de desplazamiento
scrollbar_entrada_vertical.place(x=870, y=90, height=437)

# Definir el título de la ventana
titulo_ventana = 'LFP A+ - Bryant Herrera Rubio - Proyecto 2'
raiz.title(titulo_ventana)

# Cambiar la imagen en la esquina superior izquierda de la ventana
raiz.iconbitmap('FIUSAC.ico')

# Aquí es para definir el tamaño de la ventana y centrarla
# definir tamaño de la ventana
ancho_ventana= 900
alto_ventana= 600
# Obtener información de las dimensiones de la pantalla de donde se está ejecutando el programa
ancho_pantalla = raiz.winfo_screenwidth()
alto_pantalla = raiz.winfo_screenheight()
# calcular las coordenadas en posición X y Y de la pantalla
x_pos = (ancho_pantalla - ancho_ventana) // 2
y_pos = ((alto_pantalla - alto_ventana) // 2 ) - 40
# Centrar la ventana
raiz.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

# Color de fondo de la ventana
raiz.configure(bg='lightsteelblue4')

# Evitar que la ventana se pueda redimensionar
raiz.resizable(False ,False)

# Fuente personalizada para botones
fuente_personalizada = ('Comic Sans MS', 10)

# Método mainloop() inicia el bucle de eventos, permite que la ventana esté abierta y responda a las interacciones del usuario
# La instrucción mainloop tiene que ir siempre al final
raiz.mainloop()
