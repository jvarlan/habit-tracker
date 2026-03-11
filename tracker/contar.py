import csv
from config import BASE_DIR
from .checks import normalizar

def contar_temporizador(nombre):
    
    ruta = BASE_DIR / "datos" / "temporizadores.csv"
    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
        contador = 0
        for fila in lector:
            if fila[1] == nombre:
                contador = contador + 1
    return contador

def contar_temporizador_id(id_temporizador):
    ruta = BASE_DIR / "datos" / "temporizadores.csv"
    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
        contador = 0
        for fila in lector:
            if normalizar(fila[0]) == normalizar(id_temporizador):
                contador = contador + 1
    return contador


def contar_habitos(nombre):
    ruta = BASE_DIR / "datos" / "habitos.csv"
    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
        contador = 0
        for fila in lector:
            if fila[0] == nombre:
                contador = contador + 1
    return contador

def contar_temporizador_cat(id_habito):

    ruta = BASE_DIR / "datos" / "temporizadores.csv"

    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
        contador = 0
        for fila in lector:
            if fila[1] == id_habito:
               contador = contador + 1
            else:
               return False
    return contador


def contar_id(fichero):
   
    ruta = BASE_DIR / "datos" / f"{fichero}"

    if not ruta.exists():
        return 0
    
    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        ids = [int(fila["id"]) for fila in lector]
    return max(ids, default=0) + 1
