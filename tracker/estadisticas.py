import csv
from config import BASE_DIR
from .utilidades import print_color, cumple_periodo
from datetime import datetime


def leer():
    ruta = BASE_DIR / "datos" / "habitos.csv"

    if not ruta.exists():
        return []

    with open(ruta, mode="r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        datos = list(lector)
    
    datos_transformados = [{"habito": fila["habito"], "tiempo": int(fila["tiempo"])} for fila in datos]
    return datos_transformados

def estadisticas(datos):
    for fila in datos:
        return(fila)
    

def objetivos(tipos,temporizadores, tipo_periodo, offset=0):
        ahora = datetime.now()
        variable = ""
        if offset == 0:
            variable = "Actual"
        elif offset == 1:
            variable = "Anterior"
        
        for tipo in tipos:     
            id_habito = tipo['id']
            horas_totales = 0
            for temporizador in temporizadores:
                if temporizador['id_habito'] == id_habito:
                    fecha_temp = datetime.strptime(temporizador['fecha'], "%Y-%m-%d")
                    if cumple_periodo(fecha_temp, ahora, tipo_periodo, offset):
                        
                       
                        horas_totales = horas_totales + int(temporizador['tiempo'])
            conseguido = ""
            if int(horas_totales) >= int(tipo['objetivo']):
                conseguido = "✔️"
            else:
                conseguido = "❌"

            print(f"{variable}: {tipo['habito']} -> {horas_totales}/{tipo['objetivo']} horas {conseguido}")
