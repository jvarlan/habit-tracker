import csv
from config import BASE_DIR
from datetime import datetime
from .utilidades import ROJO, print_color
import unicodedata

def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD",texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto

def comprobar_registro(habito):

    habito = normalizar(habito)
    
    ruta = BASE_DIR / "datos" / "habitos.csv"

    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        contador = 0
        for fila in lector:
            if fila[1].lower() == habito:
                contador += 1
        return int(contador)

    
def comprobar_categoria(categoria):
    ruta = BASE_DIR / "datos" / "categorias.csv"

    if not ruta.exists():
        return 0
    
    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        return any(fila["categoria"].lower() == categoria.lower() for fila in lector)
    
def comprobar_horas_temp(temporizadores, horas, fecha, nombre):
    contador_horas = 0.0
    for temporizador in temporizadores:
        if datetime.strptime(temporizador["fecha"], "%Y-%m-%d").date() == fecha and temporizador["nombre"] == nombre:
            contador_horas = contador_horas + float(temporizador["horas"])
    contador_horas = contador_horas + float(horas)
    return contador_horas

def comprobar_horas_temp_24(temporizadores, fecha, nombre):
    contador_horas = 0.0
    for temporizador in temporizadores:
        if datetime.strptime(temporizador["fecha"], "%Y-%m-%d").date() == fecha and temporizador["nombre"] == nombre:
            contador_horas = contador_horas + float(temporizador["horas"])
    return contador_horas

def validar_horas(numero):
    try:
        numero = float(numero)
    except ValueError:
        print_color("Introduce un número de horas válido.",ROJO)
        return False
    if float(numero) <= 0:
        print_color("Las horas deben ser mayores que 0",ROJO)
        return False
    else:
        return True

def validar_borrar_temporizador(borrar,lista):
  
    try:
        borrar = int(borrar)
        if borrar >= 1 and borrar <= len(lista):
            return lista[borrar - 1]
        else:
            print_color(f"Opcion no valida",ROJO)
            return None
    except ValueError:
        print_color("Debes introducir un número válido", ROJO)
        return None