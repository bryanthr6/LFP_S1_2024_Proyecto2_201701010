from analizador import tokens, Token, error_messages

# Define las clases para representar la estructura de la gramática
class Statement:
    pass

class CreateStatement(Statement):
    def __init__(self, identifier):
        self.identifier = identifier

class DeleteStatement(Statement):
    def __init__(self, identifier):
        self.identifier = identifier

class InsertStatement(Statement):
    def __init__(self, identifier, key_value_pairs):
        self.identifier = identifier
        self.key_value_pairs = key_value_pairs

class UpdateStatement(Statement):
    def __init__(self, identifier, key_value_pairs_old, key_value_pairs_new):
        self.identifier = identifier
        self.key_value_pairs_old = key_value_pairs_old
        self.key_value_pairs_new = key_value_pairs_new

class SelectStatement(Statement):
    def __init__(self, identifier):
        self.identifier = identifier

class EmptyStatement(Statement):
    pass

# Define las funciones para analizar la secuencia de tokens
def parse_create_statement(tokens):
    # Implementa la lógica para analizar una instrucción 'CrearBD' o 'CrearColeccion'
    pass

def parse_delete_statement(tokens):
    # Implementa la lógica para analizar una instrucción 'EliminarBD' o 'EliminarColeccion'
    pass

def parse_insert_statement(tokens):
    # Implementa la lógica para analizar una instrucción 'InsertarUnico'
    pass

# Define las demás funciones de análisis de instrucciones

def parse_statement(tokens):
    # Implementa la lógica para analizar una instrucción completa
    pass





# Definir una variable global para el índice actual del token
current_token_index = 0

# Función para avanzar al siguiente token
def next_token():
    global current_token_index
    current_token_index += 1

# Función para verificar si hay más tokens disponibles
def has_more_tokens():
    return current_token_index < len(tokens)

# Función para verificar si el token actual tiene el valor esperado
def expect(value):
    if has_more_tokens() and tokens[current_token_index].value == value:
        next_token()
        return True
    else:
        return False

# Reglas de la gramática del lenguaje
def statement():
    if expect("CrearBD"):
        if expect("ID"):
            return True
    elif expect("EliminarBD"):
        if expect("ID"):
            return True
    elif expect("CrearColeccion"):
        if expect("ID"):
            return True
    elif expect("EliminarColeccion"):
        if expect("ID"):
            return True
    elif expect("InsertarUnico"):
        if expect("ID"):
            if expect("{"):
                # Aquí podrías agregar más lógica para verificar la estructura del objeto JSON
                if expect("}"):
                    return True
    # Agrega más reglas según la gramática del lenguaje

    # Si ninguna regla coincide, mostrar un mensaje de error
    error_messages.append(("Error sintáctico: declaración inválida", "Error sintáctico"))
    return False

# Función principal del analizador sintáctico
def parse():
    global current_token_index
    current_token_index = 0

    # Limpiar la lista de mensajes de error
    error_messages.clear()

    # Comenzar el análisis sintáctico
    while has_more_tokens():
        statement()

    # Si hay tokens restantes después del análisis, mostrar un mensaje de error
    if current_token_index < len(tokens):
        error_messages.append(("Error sintáctico: tokens adicionales no reconocidos", "Error sintáctico"))

# Llamar a la función parse para iniciar el análisis sintáctico
parse()
