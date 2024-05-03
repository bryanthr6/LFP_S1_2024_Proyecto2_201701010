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

def parse_delete_statement(tokens):
    # Comprueba si la instrucción comienza con 'EliminarBD' o 'EliminarColeccion'
    if len(tokens) < 3:
        return None  # La instrucción es demasiado corta para ser válida
    
    if tokens[0].value == 'EliminarBD':
        if tokens[1].value != 'DBEjemplo':  # Comprueba el identificador
            return None  # El identificador no es válido
        if tokens[2].value != ';':  # Comprueba el punto y coma al final
            return None  # La instrucción no termina correctamente
        return DeleteStatement(tokens[1].value)
    
    if tokens[0].value == 'EliminarColeccion':
        # Comprueba si hay suficientes tokens para verificar la estructura de la instrucción
        if len(tokens) < 4:
            return None  # La instrucción es demasiado corta para ser válida
        
        # Verifica el identificador de la colección
        collection_identifier = tokens[1].value
        if not (collection_identifier.startswith('"') and collection_identifier.endswith('"')):
            return None  # El identificador de la colección debe estar entre comillas
        
        # Verifica el punto y coma al final
        if tokens[2].value != ';':
            return None  # La instrucción no termina correctamente
        
        return DeleteStatement(collection_identifier[1:-1])  # Retorna una instancia de DeleteStatement si es válido
    
    return None 


def parse_insert_statement(tokens):
    # Comprueba si la instrucción comienza con 'InsertarUnico'
    if len(tokens) < 8:
        return None  # La instrucción es demasiado corta para ser válida
    
    if tokens[0].value == 'InsertarUnico':
        if tokens[1].value != 'insertarFutbolista':  # Comprueba el identificador
            return None  # El identificador no es válido
        if tokens[2].value != '=' or tokens[3].value != 'new' or tokens[4].value != 'InsertarUnico' or tokens[5].value != '(':
            return None  # La estructura de la instrucción no es válida
        
        # Verifica el contenido entre paréntesis
        key_value_pairs = {}
        i = 6
        while i < len(tokens):
            if tokens[i].value == ')':
                break  # Sal del bucle si llegamos al final del contenido
            if tokens[i].value != ',':
                # Esperamos que el siguiente token sea una cadena, luego dos puntos y otra cadena
                if i + 2 < len(tokens) and tokens[i].value.startswith('"') and tokens[i + 1].value == ':' and tokens[i + 2].value.startswith('"'):
                    key = tokens[i].value[1:-1]  # Quita las comillas del principio y del final
                    value = tokens[i + 2].value[1:-1]  # Quita las comillas del principio y del final
                    key_value_pairs[key] = value
                    i += 3  # Saltamos al siguiente token después del valor
                else:
                    return None  # La estructura del par clave-valor es incorrecta
            else:
                i += 1  # Saltamos al siguiente token si encontramos una coma
        
        # Verifica si se cierra correctamente con un punto y coma
        if i + 1 < len(tokens) and tokens[i + 1].value == ';':
            return InsertStatement(tokens[1].value, key_value_pairs)  # Retorna una instancia de InsertStatement si es válido
        
    return None



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


def translate_delete_statement(statement):
    # Aquí se traduce la instrucción DeleteStatement a un comando MongoDB para eliminar la colección
    return {"drop": statement.collection_name}

# Define las demás funciones de traducción para cada tipo de instrucción

def translate_statement(statement):
    if isinstance(statement, DeleteStatement):
        return translate_delete_statement(statement)
    
    # Agrega traducciones para otros tipos de instrucciones aquí

# Ejemplo de uso:
statement = parse_delete_statement(tokens)
if statement:
    mongo_command = translate_statement(statement)
    print("Comando MongoDB:", mongo_command)
else:
    print("Instrucción no válida.")