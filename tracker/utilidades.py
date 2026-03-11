ROJO = "\033[31m"
VERDE = "\033[32m"
CIAN = "\033[36m"
INVERSION = "\033[7m"
RESET = "\033[0m"

import os
from .mostrar import mostrar_registros_todo

def print_color(texto,color):
    RESET = "\033[0m"
    print(f"{color}{texto}{RESET}")

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def preguntar_seguir(seguir):
    while True:
        if seguir in ("s", "si"):
            limpiar_pantalla()
            return True
        elif seguir in ("n", "no"):
            limpiar_pantalla()
            return False
        else:
            print("Respuesta no válida.")
            break
        
def id_habito_nombre():

    # crea un diccionario vacio
    id_habito_nombre = {}
    # saca del csv todos los habitos registrados y sus campos
    habitos = mostrar_registros_todo()
    for habito in habitos:
        #guarda en el diccionario el equivalente del id_habito a su nombre
        id_habito_nombre[habito[0]] = habito[1]
    return id_habito_nombre

def nombre_idhabito():

    # crea un diccionario vacio
    id_habito_nombre = {}
    # saca del csv todos los habitos registrados y sus campos
    habitos = mostrar_registros_todo()
    for habito in habitos:
        #guarda en el diccionario el equivalente del id_habito a su nombre
        id_habito_nombre[habito[1]] = habito[0]
    return id_habito_nombre