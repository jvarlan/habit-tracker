import csv
from config import BASE_DIR
from datetime import datetime
from .utilidades import ROJO, NARANJA, print_color, horas_a_segundos, normalizar, input_color
from .mostrar import mostrar_temporizadores




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
    
def comprobar_horas_temp(horas_str, fecha, id_habito):

    if not validar_horas(horas_str):
        return False
    
    total_segundos = horas_a_segundos(horas_str)

    temporizadores = mostrar_temporizadores()
    contador_segundos = 0.0
    for temporizador in temporizadores:
        if datetime.strptime(temporizador["fecha"], "%Y-%m-%d").date() == fecha and temporizador["id_habito"] == id_habito:
            contador_segundos += horas_a_segundos(temporizador["horas"])

    contador_segundos += total_segundos

    return contador_segundos

def comprobar_horas_temp_24(fecha, id_habito):
   
    temporizadores = mostrar_temporizadores()
    contador_segundos = 0

    for temporizador in temporizadores:
        if datetime.strptime(temporizador["fecha"], "%Y-%m-%d").date() == fecha and temporizador["id_habito"] == id_habito:
            horas_str = temporizador["horas"]            
            contador_segundos += horas_a_segundos(horas_str)

    return contador_segundos

def validar_horas(numero):
    
    partes = numero.split(":")
    if len(partes) not in (1,2,3):
        return False
    try:
        valores = list(map(int, partes))
    except ValueError:
            return False
    #horas
    if len(valores) == 1:
        h = valores[0]
        if h <=0:
            return False
        return f"{h:02d}:00:00"
    #horas y minutos
    elif len(valores) == 2:
        h, m = valores
        if m == 60:
            h += 1
            m = 0
        if h <0 or not (0 <=m < 60):
            return False
        return f"{h:02d}:{m:02d}:00"
    #horas, minutos y segundos
    else:
        h, m, s = valores
        if m == 60:
            h += 1
            m = 0
        if s == 60:
            m += 1
            s = 0
        if h <0 or not (0 <=m < 60) or not (0 <= s < 60):
            return False
        return f"{h:02d}:{m:02d}:{s:02d}"
    

def validar_borrar_temporizador(borrar,lista):
  
  # sirve para validar borrar temporizador y objetivos
    try:
        borrar = int(borrar)
        if borrar >= 1 and borrar <= len(lista):
            return lista[borrar - 1]
        else:
            print_color(f"Opción no valida",ROJO)
            return None
    except ValueError:
        print_color("\nDebes introducir un número válido: ", NARANJA)
        return None
