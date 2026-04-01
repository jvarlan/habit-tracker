import csv
from config import BASE_DIR
from .utilidades import print_color, print_color_pausa, cumple_periodo, imprimir_con_pausa, ROJO, VERDE, CIAN
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
        lineas = []
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

            linea = f"{tipo['habito']} -> {horas_totales}/{tipo['objetivo']} horas {conseguido}"
            lineas.append(linea)

        return lineas
def media_objetivos(tipos,temporizadores, tipo_periodo, num_periodos):
        ahora = datetime.now()
        lineas = []
        for tipo in tipos:     
            id_habito = tipo['id']
            horas_totales = 0
            for offset in range(num_periodos):
                for temporizador in temporizadores:
                    if temporizador['id_habito'] == id_habito:
                        fecha_temp = datetime.strptime(temporizador['fecha'], "%Y-%m-%d")
                        if cumple_periodo(fecha_temp, ahora, tipo_periodo, offset):
                            horas_totales = horas_totales + int(temporizador['tiempo'])
            conseguido = ""
            horas_totales = horas_totales / num_periodos
            if int(horas_totales) >= int(tipo['objetivo']):
                conseguido = "✔️"
            else:
                conseguido = "❌"

            linea = f"{tipo['habito']} -> {horas_totales:.2f}/{tipo['objetivo']} horas {conseguido}"
            lineas.append(linea)

        return lineas

def generar_bloque_objetivo(titulo,datos,temporizadores,tipo,unidad,media_n):
    if not datos:
        print_color(f"No hay objetivos {titulo}",ROJO)
        return []
    return [
        print_color_pausa(f"\nObjetivos {titulo}: ",VERDE),
        f"\n{unidad} actual: ",
        *objetivos(datos, temporizadores, tipo, 0),
        f"\n{unidad} anterior: ",
        *objetivos(datos, temporizadores, tipo, 1),
        f"\nMedia últimos {media_n} {titulo}: ",
        *media_objetivos(datos, temporizadores, tipo, media_n),
    ]

def generar_bloque_resumen(titulo,datos,temporizadores,tipo,unidad,media_n):
    print(datos)
    if not datos:
        print_color(f"No hay objetivos {titulo}",ROJO)
        return []
    return [
        print_color_pausa(f"\nObjetivos {titulo}: ",VERDE),
        *objetivos(datos, temporizadores, tipo, 0),
    ]
