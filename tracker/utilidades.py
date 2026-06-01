ROJO = "\033[31m"
VERDE = "\033[32m"
CIAN = "\033[36m"
INVERSION = "\033[7m"
RESET = "\033[0m"

import os, shutil
import time
from .mostrar import mostrar_csv, mostrar_csv_diccionario

from datetime import timedelta, datetime

def print_color(texto,color):
    RESET = "\033[0m"
    print(f"{color}{texto}{RESET}")
def print_color_pausa(texto,color):
    RESET = "\033[0m"
    return f"{color}{texto}{RESET}"

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def preguntar_seguir(seguir):
        seguir = seguir.lower().strip()
        if seguir in ("s", "si"):
            return True
        elif seguir in ("n", "no"):
            return False
        else:
            return None
        
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


def cumple_periodo(fecha, ahora, tipo, offset):
   

    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
    if isinstance(ahora, datetime):
        ahora = ahora.date()

    if tipo == "dia":
        return fecha == (ahora - timedelta(days=offset))

    elif tipo == "semana":
        referencia = ahora - timedelta(weeks=offset)
        return fecha.isocalendar().week == referencia.isocalendar().week and fecha.year == referencia.year
   
    elif tipo == "mes":
        mes = ahora.month - offset
        año = ahora.year

        while mes <= 0:
            mes += 12
            año -= 1

        return fecha.year == año and fecha.month == mes

    elif tipo == "año":

        return fecha.year == (ahora.year - offset)


def imprimir_con_pausa(lineas):
    try:
        altura = shutil.get_terminal_size().lines - 9 #margen de lineas
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
    objetivos = mostrar_csv_diccionario("objetivos")

    diarios = [h for h in objetivos if h.get("tipo","").strip().lower() == "diario"]
    semanales = [h for h in objetivos if h.get("tipo","").strip().lower() == "semanal"]
    mensuales = [h for h in objetivos if h.get("tipo","").strip().lower() == "mensual"]
    anuales = [h for h in objetivos if h.get("tipo","").strip().lower() == "anual"]

    return diarios, semanales, mensuales, anuales, habitos, temporizadores, categorias

def cronometro(stop_event, resultado):

    inicio = time.time()

    while not stop_event.is_set():

        tiempo = time.time() - inicio
        horas = int(tiempo // 3600)
        minutos = int((tiempo % 3600) // 60)
        segundos = int(tiempo % 60)

        print(f"\rTiempo: {horas:02d}:{minutos:02d}:{segundos:02d}",end="")
        time.sleep(1)
    print()
    resultado.append(f"{horas:02d}:{minutos:02d}:{segundos:02d}")

def esperar_enter(stop_event):
    input()
    stop_event.set()

def horas_a_segundos(horas_str):
    """Convierte un string 'HH:MM:SS' a segundos totales"""
    h, m, s = map(int, horas_str.split(":"))
    return h * 3600 + m * 60 + s

def segundos_a_hhmmss(segundos):
    """Convierte segundos a string HH:MM:SS"""
    h = segundos // 3600
    m = (segundos % 3600) // 60
    s = segundos % 60
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"

def horas_string_a_HHMM(numero_str):

    numero = float(numero_str)  # aseguras entero

    horas = int(numero)
    minutos = int((numero - horas) * 60)
    segundos = int((((numero - horas) * 60) - minutos) * 60)

    hhmm = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    return hhmm

def numero_string_a_HHMM(numero_str):
    numero = int(float(numero_str))  # aseguras entero

    horas = numero // 3600
    minutos = (numero % 3600) // 60
    segundos = numero % 60

    hhmm = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    return hhmm