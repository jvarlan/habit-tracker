import csv
from config import BASE_DIR
from datetime import datetime

def dev_habito_id(habito):
    
    from .utilidades import normalizar

    ruta = BASE_DIR / "datos" / "habitos.csv"
    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            if normalizar(fila[1]) == normalizar(habito):
                return fila[0]
            
def dev_habito_datos(habito):
    from .utilidades import normalizar

    ruta = BASE_DIR / "datos" / "habitos.csv"
    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
       
        for fila in lector:
            if normalizar(fila['habito']) == normalizar(habito):
                return fila
            
def dev_tipo_objetivo(id_habito):
    from .utilidades import normalizar

    ruta = BASE_DIR / "datos" / "objetivos.csv"
    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
        lista = []
        for fila in lector:
            if normalizar(fila[1]) == normalizar(id_habito):
                lista.append(fila[2])
        return lista


def dev_nombre_habito_id(id_habito):
    from .utilidades import normalizar

    ruta = BASE_DIR / "datos" / "habitos.csv"
    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            if normalizar(fila[0]) == normalizar(id_habito):
                return fila[1]
                     
def dev_temporizador_id(temporizador):
    from .utilidades import normalizar

    ruta = BASE_DIR / "datos" / "temporizadores.csv"

    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            if normalizar(fila[2]) == normalizar(temporizador):
                return fila[0]
def dev_idhabito_temporizador(id_temporizador):
    from .utilidades import normalizar

    ruta = BASE_DIR / "datos" / "temporizadores.csv"
    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            if normalizar(fila[0]) == normalizar(id_temporizador):
                return fila[1]
                        
def dev_lista_habitos_cat(id_categoria):
    from .utilidades import normalizar
    
    ruta = BASE_DIR / "datos" / "habitos.csv"

    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
        lista = []
        for fila in lector:
            if normalizar(fila[2]) == normalizar(id_categoria):
                lista.append(fila) 
        return lista  
    
def dev_lista_temporizadores_cat(lista_habitos):
    from .utilidades import normalizar

    ruta = BASE_DIR / "datos" / "temporizadores.csv"
    
    lista_habitos_id = [normalizar(habito[0]) for habito in lista_habitos]

    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
        lista = []
        for fila in lector:
            if normalizar(fila[1]) in lista_habitos_id:
                lista.append(fila) 
        return lista  
            
def dev_lista_objetivos_cat(lista_habitos):
    from .utilidades import normalizar
    
    ruta = BASE_DIR / "datos" / "objetivos.csv"
    
    lista_habitos_id = [normalizar(habito[0]) for habito in lista_habitos]

    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
        lista = []
        for fila in lector:
            if normalizar(fila[1]) in lista_habitos_id:
                lista.append(fila) 
        return lista  


def dev_categoria_id(categoria):
    from .utilidades import normalizar

    ruta = BASE_DIR / "datos" / "categorias.csv"

    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            if normalizar(fila[1]) == normalizar(categoria):
                return fila[0]

def dev_nombre_categoria_id(id_categoria):
    
    from .utilidades import normalizar

    ruta = BASE_DIR / "datos" / "categorias.csv"
    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            if normalizar(fila[0]) == normalizar(id_categoria):
                return fila[1]


def dev_emoticono_categoria_id(id_categoria):
    from .utilidades import normalizar

    ruta = BASE_DIR / "datos" / "categorias.csv"
    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            if normalizar(fila[0]) == normalizar(id_categoria):
                return fila[2]
            
def dev_id_categoria_habito_id(id_habito):

    from .utilidades import normalizar

    ruta = BASE_DIR / "datos" / "habitos.csv"
    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            if normalizar(fila[0]) == normalizar(id_habito):
                return fila[2]

def dev_habito_correcto(habito):
    
    from .utilidades import normalizar

    ruta = BASE_DIR / "datos" / "habitos.csv"
    if not ruta.exists():
        return 0

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
       
        for fila in lector:
            if normalizar(fila[1]) == normalizar(habito):
                return fila[1]

def dev_categoria_correcta(categoria):

    from .utilidades import normalizar

    ruta = BASE_DIR / "datos" / "categorias.csv"

    if not ruta.exists():
        return categoria

    with open(ruta, newline="", encoding="utf-8") as archivo:

        lector = csv.reader(archivo)
        next(lector, None)

        for fila in lector:

            if normalizar(fila[1]) == normalizar(categoria):
                return fila[1]

    # Si la categoría no existe, devuelve la introducida
    return categoria