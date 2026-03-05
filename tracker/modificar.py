import csv
from config import BASE_DIR
from .checks import normalizar
from .utilidades import ROJO, VERDE, RESET

def modificar_habito(modificar,id_modificar):
    ruta = BASE_DIR / "datos" / "habitos.csv"

    if not ruta.exists():
        return 0
    filas_restantes = []
    filas_originales = []

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            
            if fila[0] == id_modificar:
                fila_modificada = [fila[0],modificar,fila[2],fila[3]]
                filas_restantes.append(fila_modificada)
            else:
                filas_restantes.append(fila)
                filas_originales.append(fila)

    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(filas_restantes)

    if len(filas_originales) == len(filas_restantes):
        return (f"{ROJO}El registro '{modificar}' no existe.{RESET}")
    else:
        return (f"{ROJO}Registro '{modificar}' modificado.{RESET}")
    
def borrar_temporizador(borrar,seleccion):
    ruta = BASE_DIR / "datos" / "temporizadores.csv"

    if not ruta.exists():
        return 0
    filas_restantes = []
    filas_originales = []

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            filas_originales.append(fila)
            if normalizar(fila[0]) != borrar:
                filas_restantes.append(fila)
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(filas_restantes)

    if len(filas_originales) == len(filas_restantes):
        return (f"{ROJO}El registro '{seleccion}' no existe.{RESET}")
    else:
        return (f"{VERDE}Registro '{seleccion}' eliminado.{RESET}")
    
def modificar_temporizadores(id_habito,temporizador):
    ruta = BASE_DIR / "datos" / "temporizadores.csv"
    if not ruta.exists():
        return 0
    filas_restantes = []
    filas_originales = []

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            filas_originales.append(fila)
            if fila[1] != id_habito:
                filas_restantes.append(fila)
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(filas_restantes)

    if len(filas_originales) == len(filas_restantes):
        return (f"{ROJO}El temporizador '{temporizador}' no existe.{RESET}")
    else:
        return (f"{VERDE}Todos los temporizadores asociados a '{temporizador}' han sido eliminados.{VERDE}")
def borrar_categoria(borrar,id_categoria,lista_habitos,lista_temporizadores):
    
    for habitos in lista_habitos:
        borrar_habito(habitos[1],habitos[0])
    for temporizadores in lista_temporizadores:
        borrar_temporizador(temporizadores[0],temporizadores[2])
    ruta = BASE_DIR / "datos" / "categorias.csv"

    if not ruta.exists():
        return 0
    filas_restantes = []
    filas_originales = []

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            filas_originales.append(fila)
            if normalizar(fila[0]) != id_categoria:
                filas_restantes.append(fila)
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(filas_restantes)

    if len(filas_originales) == len(filas_restantes):
        return (f"{ROJO}La categoría '{borrar}' no existe.{RESET}")
    else:
        return (f"{ROJO}La categoría '{borrar}' ha sido eliminada.{RESET}")

def borrar_csv(fichero):
    ruta = BASE_DIR / "datos" / f"{fichero}"

    open(ruta, "w").close()