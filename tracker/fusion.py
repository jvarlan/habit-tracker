import csv
from config import BASE_DIR
from .utilidades import ROJO, VERDE, RESET, normalizar

def fusionar_habitos(id_principal, id_secundario):

    ruta = BASE_DIR / "datos" / "habitos.csv"
    
    if not ruta.exists():
        return 0
    
    filas_restantes = []
    filas_originales = []
    
    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            
            if fila[0] == id_secundario:
                continue  # Omitir la fila del hábito fusionado
            else:
                filas_restantes.append(fila)
                filas_originales.append(fila)

    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(filas_restantes)

    if len(filas_originales) == len(filas_restantes):
        return (f"{ROJO}El registro '{id_secundario}' no existe.{RESET}")
    else:
        return (f"{VERDE}Registro '{id_secundario}' fusionado con '{id_principal}'.{RESET}")
    
def fusionar_objetivos(id_principal, id_secundario):

    ruta = BASE_DIR / "datos" / "objetivos.csv"
    
    if not ruta.exists():
        return 0
    
    filas_restantes = []
    filas_originales = []
    
    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)    
        for fila in lector:
            
            if fila[0] == id_secundario:
                continue
            else:
                filas_restantes.append(fila)
                filas_originales.append(fila)

    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(filas_restantes)

    if len(filas_originales) == len(filas_restantes):
        return (f"{ROJO}El registro '{id_secundario}' no existe.{RESET}")
    else:
        return (f"{VERDE}Registro '{id_secundario}' fusionado con '{id_principal}'.{RESET}")

def fusionar_temporizadores(id_principal, id_secundario):

    ruta = BASE_DIR / "datos" / "temporizadores.csv"
    
    if not ruta.exists():
        return 0
    
    filas_restantes = []
    filas_originales = []
    
    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            
            if fila[1] == id_secundario:
                fila_modificada = [fila[0],id_principal,fila[2],fila[3]]
                filas_restantes.append(fila_modificada)   # Omitir la fila del temporizador fusionado
            else:
                filas_restantes.append(fila)
                filas_originales.append(fila)

    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(filas_restantes)

    if len(filas_originales) == len(filas_restantes):
        return (f"{ROJO}El registro '{id_secundario}' no existe.{RESET}")
    else:
        return (f"{VERDE}Registro '{id_secundario}' fusionado con '{id_principal}'.{RESET}")

def fusionar_categorias(id_principal, id_secundario):
    
    ruta = BASE_DIR / "datos" / "categorias.csv"
    
    if not ruta.exists():
        return 0
    
    filas_restantes = []
    filas_originales = []
    
    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            
            if fila[0] == id_secundario:
                continue  # Omitir la fila de la categoría fusionada
            else:
                filas_restantes.append(fila)
                filas_originales.append(fila)

    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(filas_restantes)

    if len(filas_originales) == len(filas_restantes):
        return (f"{ROJO}El registro '{id_secundario}' no existe.{RESET}")
    else:
        return (f"{VERDE}Registro '{id_secundario}' fusionado con '{id_principal}'.{RESET}")

def fusionar_habitos_categoria(id_principal, id_secundario):
    ruta = BASE_DIR / "datos" / "habitos.csv"
    
    if not ruta.exists():
        return 0
    
    filas_restantes = []
    filas_originales = []
    
    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            
            if fila[2] == id_secundario:
                fila_modificada = [fila[0],fila[1],id_principal]
                filas_restantes.append(fila_modificada)   # Omitir la fila del hábito fusionado
            else:
                filas_restantes.append(fila)
                filas_originales.append(fila)

    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(filas_restantes)

    if len(filas_originales) == len(filas_restantes):
        return (f"{ROJO}El registro '{id_secundario}' no existe.{RESET}")
    else:
        return (f"{VERDE}Registro '{id_secundario}' fusionado con '{id_principal}'.{RESET}")
