from collections import namedtuple
import re

# Definir la tupla Token
Token = namedtuple("Token", ["value", "line", "col"])

# Función para manejar tokens encontrados y clasificados
def handle_token(token):
    global tokens
    tokens.append(token)
    print(f"Token: {token.value}, Línea: {token.line}, Columna: {token.col}")


# Función para manejar caracteres desconocidos como errores y guardar los mensajes de error
def handle_unknown_character(char):
    global line, col, error_messages
    error_message = f"Error: Carácter desconocido '{char}' en línea: {line}, columna: {col}"
    print(error_message)
    error_messages.append(error_message)

# Función para tokenizar la entrada
def tokenize_input(input_str):
    global line, col

    line = 1
    col = 1
    i = 0
    while i < len(input_str):
        char = input_str[i]

        # Manejo de caracteres especiales
        if char.isspace():
            if char == "\n":
                line += 1
                col = 1
            elif char == "\t":
                col += 4
            i += 1
        elif char in ["{", "}", "[", "]", ",", ";"]:
            col += 1
            token = Token(char, line, col)
            handle_token(token)
            i += 1
        elif char == "=":
            col += 1
            # Manejar operador de asignación o comparación
            if i + 1 < len(input_str) and input_str[i + 1] == "=":
                token = Token("==", line, col)
                handle_token(token)
                i += 2
            else:
                token = Token(char, line, col)
                handle_token(token)
                i += 1
        elif char == "/":
            col += 1
            # Manejar comentarios de una línea
            if i + 1 < len(input_str) and input_str[i + 1] == "/":
                while i < len(input_str) and input_str[i] != "\n":
                    i += 1
                line += 1
                col = 1
            # Manejar comentarios de varias líneas
            elif i + 1 < len(input_str) and input_str[i + 1] == "*":
                while i < len(input_str) - 1 and (input_str[i] != "*" or input_str[i + 1] != "/"):
                    if input_str[i] == "\n":
                        line += 1
                        col = 1
                    else:
                        col += 1
                    i += 1
                if i < len(input_str) - 1:
                    i += 2
                    col += 2
                else:
                    handle_unknown_character(char)
                    i += 1
            else:
                token = Token(char, line, col)
                handle_token(token)
                i += 1
        elif char == '"':
            # Tokenizar cadenas entre comillas
            token, pos = tokenize_string(input_str[i:], line, col)
            handle_token(token)
            col += pos
            i += pos
        elif char.isdigit():
            # Tokenizar números
            token, pos = tokenize_number(input_str[i:], line, col)
            handle_token(token)
            col += pos
            i += pos
        elif char.isalpha():
            # Tokenizar palabras clave e identificadores
            token, pos = tokenize_keyword(input_str[i:], line, col)
            handle_token(token)
            col += pos
            i += pos
        else:
            handle_unknown_character(char)
            col += 1
            i += 1

# Función para tokenizar cadenas entre comillas
def tokenize_string(input_str, line, col):
    token = '"'
    i = 1
    while i < len(input_str):
        char = input_str[i]
        token += char
        if char == '"':
            return Token(token, line, col), i + 1
        i += 1
        col += 1
    return Token(token, line, col), i

# Función para tokenizar números
def tokenize_number(input_str, line, col):
    token = ""
    i = 0
    while i < len(input_str):
        char = input_str[i]
        if char.isdigit() or char == ".":
            token += char
            if char == ".":
                is_float = True
        else:
            break
        i += 1
        col += 1
    if token.count(".") > 1:
        print("Error: Número decimal inválido en línea:", line, "columna:", col - len(token))
    if token.startswith(".") or token.endswith("."):
        print("Error: Punto decimal mal colocado en línea:", line, "columna:", col - len(token))
    return Token(token, line, col - len(token)), i

# Función para tokenizar palabras clave e identificadores
def tokenize_keyword(input_str, line, col):
    token = ""
    i = 0
    while i < len(input_str):
        char = input_str[i]
        if char.isalnum() or char == "_":
            token += char
        else:
            break
        i += 1
        col += 1
    return Token(token, line, col - len(token)), i

# Texto a analizar
texto = """
CrearBD DBEjemplo = new CrearBD();
EliminarBD DBEjemplo = new EliminarBD();
CrearBD Futbol = new CrearBD();
CrearColeccion nuevaColeccion = new CrearColeccion("Calificacion");
EliminarColeccion eliminarColeccion = new EliminarColeccion("Calificacion");
CrearColeccion nuevaColeccion = new CrearColeccion("Futbolistas");
--- Messi el único GOAT
InsertarUnico insertarFutbolista = new InsertarUnico("Futbolistas", 
{ 
    "nombre": "Lionel Messi",
    "club": "Paris Saint-Germain"
}
/* 
	Es que Haaland es muy bueno también, pero bueno, centrémonos en LFP :D
*/
BuscarTodo todosFutbolistas = new BuscarTodo("Futbolistas");
BuscarUnico unFutbolista = new BuscarUnico("Futbolistas");
InsertarUnico insertarFutbolista = new InsertarUnico("Futbolistas", 
{ 
    "nombre": "Erling Haaland",
    "club": "Manchester City"
}
);
ActualizarUnico actualizarFutbolista = new ActualizarUnico("Futbolistas", 
{
    "nombre": "Lionel Messi" 
}, 
{ 
     $set: { "club": "Inter Miami" } 
}
);
BuscarTodo todosFutbolistas = new BuscarTodo("Futbolistas");
BuscarUnico unFutbolista = new BuscarUnico("Futbolistas");
EliminarUnico eliminarFutbolista = new EliminarUnico("Futbolistas", 
{ 
     "nombre": "Lionel Messi" 
}
);
BuscarTodo todosFutbolistas = new BuscarTodo("Futbolistas");
BuscarUnico unFutbolista = new BuscarUnico("Futbolistas");
/* 
	Eliminamos a Haaland para verificar el flujo de información
*/
EliminarUnico eliminarFutbolista2 = new EliminarUnico("Futbolistas",
{
      "nombre": "Erling Haaland"
}
);
/* 
	No debería de haber nada en la colección
*/
BuscarTodo todosFutbolistas = new BuscarTodo("Futbolistas");
BuscarUnico unFutbolista = new BuscarUnico("Futbolistas");
--- Si llegaste hasta acá felicidades, trabajaste duro :')
"""

# Inicializar variables globales
tokens = []
error_messages = []

# Tokenizar el texto de entrada
tokenize_input(texto)

