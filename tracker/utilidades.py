ROJO = "\033[31m"
VERDE = "\033[32m"
CIAN = "\033[36m"
INVERSION = "\033[7m"
RESET = "\033[0m"

import os, shutil
from .mostrar import mostrar_csv, mostrar_csv_diccionario
from datetime import timedelta

def print_color(texto,color):
    RESET = "\033[0m"
    print(f"{color}{texto}{RESET}")
def print_color_pausa(texto,color):
    RESET = "\033[0m"
    return f"{color}{texto}{RESET}"

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
    habitos = mostrar_csv("habitos")
    for habito in habitos:
        #guarda en el diccionario el equivalente del id_habito a su nombre
        id_habito_nombre[habito[0]] = habito[1]
    return id_habito_nombre

def nombre_idhabito():

    # crea un diccionario vacio
    id_habito_nombre = {}
    # saca del csv todos los habitos registrados y sus campos
    habitos = mostrar_csv("habitos")
    for habito in habitos:
        #guarda en el diccionario el equivalente del id_habito a su nombre
        id_habito_nombre[habito[1]] = habito[0]
    return id_habito_nombre

def cumple_periodo(fecha, ahora, tipo, offset=0):

    if tipo == "dia":
        referencia = ahora - timedelta(days=offset)
        return fecha.date() == referencia.date()

    elif tipo == "semana":
        referencia = ahora - timedelta(weeks=offset)
        a1, s1, _ = fecha.isocalendar()
        a2, s2, _ = referencia.isocalendar()
        return a1 == a2 and s1 == s2

    elif tipo == "mes":
        mes = ahora.month - offset
        año = ahora.year

        while mes <= 0:
            mes += 12
            año -= 1

        return fecha.year == año and fecha.month == mes

    elif tipo == "año":
        return fecha.year == (ahora.year - offset)

    return False

def imprimir_con_pausa(lineas):
    try:
        altura = shutil.get_terminal_size().lines - 10 #margen de lineas
    except:
        altura = 20

    contador = 0

    for linea in lineas:
        print(linea)
        contador +=1

        if contador >= altura:
            input(print_color_pausa("\nPulsa ENTER para continuar... \n",ROJO))
            limpiar_pantalla()
            contador = 0

def volver_atras(texto):
    if texto in ("","volver","salir"):
        return False
    
def agrupar_datos_csv():
    habitos = mostrar_csv_diccionario("habitos")
    temporizadores = mostrar_csv_diccionario("temporizadores")
    categorias = mostrar_csv_diccionario("categorias")

    diarios = [h for h in habitos if h.get("tipo","").strip().lower() == "diario"]
    semanales = [h for h in habitos if h.get("tipo","").strip().lower() == "semanal"]
    mensuales = [h for h in habitos if h.get("tipo","").strip().lower() == "mensual"]
    anuales = [h for h in habitos if h.get("tipo","").strip().lower() == "anual"]

    return diarios, semanales, mensuales, anuales, habitos, temporizadores, categorias