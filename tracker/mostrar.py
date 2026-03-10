import csv
from config import BASE_DIR

def mostrar_registros(temporizador = None):
    
    ruta = BASE_DIR / "datos" / "habitos.csv"

    if not ruta.exists():
        return 0
    contador = 0
    lista = []

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            contador +=1
            lista.append(fila[1])
    return lista

def mostrar_registros_todo(temporizador = None):
    
    ruta = BASE_DIR / "datos" / "habitos.csv"

    if not ruta.exists():
        return 0
    contador = 0
    lista = []

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            contador +=1
            lista.append(fila)
    return lista


def mostrar_temporizadores():
    
    ruta = BASE_DIR / "datos" / "temporizadores.csv"

    if not ruta.exists():
        return 0
    contador = 0
    temporizadores = []

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            contador +=1
            temporizadores.append({
                "id": fila[0],
                "id_habito": fila[1],
                "nombre": fila[2],
                "horas": fila[3],
                "fecha": fila[4]
                })
    return temporizadores

def mostrar_temporizadores_todo():
    
    ruta = BASE_DIR / "datos" / "temporizadores.csv"

    if not ruta.exists():
        return 0
    contador = 0
    lista = []

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            contador +=1
            lista.append(fila)
    return lista

def mostrar_categorias(temporizador = None):
    
    ruta = BASE_DIR / "datos" / "categorias.csv"

    if not ruta.exists():
        return 0
    contador = 0
    lista = []

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            contador +=1
            lista.append(fila[1])
    return lista


