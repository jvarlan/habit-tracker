import csv
from config import BASE_DIR

def dev_habito_id(habito):
    ruta = BASE_DIR / "datos" / "habitos.csv"
    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            if fila[1].lower() == habito.lower():
                return fila[0]
def dev_nombre_habito_id(id_habito):

    ruta = BASE_DIR / "datos" / "habitos.csv"
    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            if fila[0].lower() == id_habito:
                return fila[1]
                     
def dev_temporizador_id(temporizador):
    ruta = BASE_DIR / "datos" / "temporizadores.csv"

    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            if fila[2] == temporizador:
                return fila[0]
            
def dev_lista_habitos_cat(id_categoria):
    ruta = BASE_DIR / "datos" / "habitos.csv"

    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
        lista = []
        for fila in lector:
            if fila[2] == id_categoria:
                lista.append(fila) 
        return lista  
    
def dev_lista_temporizadores_cat(lista_habitos,id_categoria):
    ruta = BASE_DIR / "datos" / "temporizadores.csv"
    
    lista_habitos_id = [habito[0] for habito in lista_habitos]

    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
        lista = []
        for fila in lector:
            if fila[1] in lista_habitos_id:
                lista.append(fila) 
        return lista  
            
def dev_categoria_id(categoria):
    ruta = BASE_DIR / "datos" / "categorias.csv"

    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            if fila[1].lower() == categoria.lower():
                return fila[0]

