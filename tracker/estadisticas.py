import csv
from config import BASE_DIR
from .utilidades import print_color, print_color_pausa, cumple_periodo, numero_string_a_HHMM, ROJO, VERDE, CIAN, segundos_a_hhmmss, horas_a_segundos, horas_string_a_HHMM
from .mostrar import mostrar_csv_diccionario
from datetime import datetime, timedelta


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
        # saca los datos de los objetivos
        ahora = datetime.now()
        lineas = []
        for tipo in tipos:  
             
            id_habito = tipo['id']
            segundos_totales = 0

            categorias = mostrar_csv_diccionario("categorias")  
                   
            id_categoria = int(tipo['id_categoria'])-1  
            emoticono_categoria = categorias[id_categoria]["emoticono"]
            
            for temporizador in temporizadores:
                if temporizador['id_habito'] == id_habito:
                    fecha_temp = datetime.strptime(temporizador['fecha'], "%Y-%m-%d")
                    if cumple_periodo(fecha_temp, ahora, tipo_periodo, offset):
                        segundos_totales = segundos_totales + horas_a_segundos(temporizador['tiempo'])

         
            conseguido = ""
           
            if int(segundos_totales) >= int(horas_a_segundos(tipo['objetivo'])):
                conseguido = "✔️"
            else:
                conseguido = "❌"
            
            linea = f"{emoticono_categoria} {tipo['habito']} -> {numero_string_a_HHMM(segundos_totales)}/{tipo['objetivo']} horas {conseguido}"
            lineas.append(linea)

        return lineas
def media_objetivos(tipos,temporizadores, tipo_periodo, num_periodos):
        # calcula la media dependiendo del tipo de periodo que sea (diario, semanal, mensual, anual)
        ahora = datetime.now()
        lineas = []
        for tipo in tipos:     
            id_habito = tipo['id']
            segundos_totales = 0
            for offset in range(num_periodos):
                for temporizador in temporizadores:
                    if temporizador['id_habito'] == id_habito:
                        fecha_temp = datetime.strptime(temporizador['fecha'], "%Y-%m-%d")
                        if cumple_periodo(fecha_temp, ahora, tipo_periodo, offset):
                            segundos_totales = segundos_totales + horas_a_segundos(temporizador['tiempo'])
            conseguido = ""
            segundos_totales = segundos_totales / num_periodos
            if int(segundos_totales) >= int(horas_a_segundos(tipo['objetivo'])) * 3600:
                conseguido = "✔️"
            else:
                conseguido = "❌"
            
            linea = f"{tipo['habito']} -> {numero_string_a_HHMM(segundos_totales)}/{tipo['objetivo']} horas {conseguido}"
            lineas.append(linea)

        return lineas

def generar_bloque_objetivo(titulo,datos,temporizadores,tipo,unidad,media_n):
    if not datos:
        print_color(f"No hay objetivos {titulo}",ROJO)
        return []
    return [
        print_color_pausa(f"\nObjetivo {titulo}: ",VERDE),
        print_color_pausa(f"\n{unidad} actual",CIAN),
        print_color_pausa("────────────────────────",CIAN),
   
        *objetivos(datos, temporizadores, tipo, 0),
        print_color_pausa(f"\n{unidad} anterior",CIAN),
        print_color_pausa("────────────────────────",CIAN),
        *objetivos(datos, temporizadores, tipo, 1),
        print_color_pausa(f"\nMedia últimos {media_n} {titulo}",CIAN),
        print_color_pausa("────────────────────────",CIAN),
        *media_objetivos(datos, temporizadores, tipo, media_n),
    ]
def generar_bloque_categorias(habitos,temporizadores, categorias):
    
    if not categorias:
        print_color(f"No hay objetivos",ROJO)
        return []
    return [
        print_color_pausa(f"\nHoy",VERDE),
        print_color_pausa("────────────────────────",VERDE),
        *categorias_fecha(habitos, temporizadores, categorias,"dia"),
        print_color_pausa(f"\nSemana actual",VERDE),
        print_color_pausa("────────────────────────",VERDE),
        *categorias_fecha(habitos, temporizadores, categorias,"semana"),
        print_color_pausa(f"\nMes actual",VERDE),
        print_color_pausa("────────────────────────",VERDE),
        *categorias_fecha(habitos, temporizadores, categorias,"mes"),
        print_color_pausa(f"\nAño actual",VERDE),
        print_color_pausa("────────────────────────",VERDE),
        *categorias_fecha(habitos, temporizadores, categorias,"año"),
        print_color_pausa(f"\Histórico acumulado",VERDE),
        print_color_pausa("────────────────────────",VERDE),
        *categorias_est(habitos, temporizadores, categorias),
    ]

def generar_bloque_resumen(titulo,datos,temporizadores,tipo, categorias):
    
    if not datos:
        print_color(f"No hay objetivos {titulo}",ROJO)
        return []
    return [
        print_color_pausa(f"\n{titulo}",VERDE),
        print_color_pausa("────────────────────────",VERDE),
        *resumen_est(datos, categorias, temporizadores, tipo, 0),
    ]

def resumen_est(tipos, categorias, temporizadores, tipo_periodo, offset=0):
        ahora = datetime.now()
        lineas = []
        for tipo in tipos:     
            id_habito = tipo['id']
            segundos_totales = 0
            for temporizador in temporizadores:
                if temporizador['id_habito'] == id_habito:
                    fecha_temp = datetime.strptime(temporizador['fecha'], "%Y-%m-%d")
                    if cumple_periodo(fecha_temp, ahora, tipo_periodo, offset):
                        segundos_totales = segundos_totales + horas_a_segundos(temporizador['tiempo'])

            # Icono de la categoría (💪, 🎮, 📖)
            id_categoria_habito = int(tipo['id_categoria'])-1
           
            emoticono_categoria = categorias[id_categoria_habito]["emoticono"]

            porcentaje = (float(segundos_totales) / (float(horas_a_segundos(tipo['objetivo'])))) * 100

            if porcentaje == 0:
                objetivo = "👎"
            elif porcentaje > 0 and porcentaje <= 50:
                objetivo = "📈"
            elif porcentaje > 50 and porcentaje <= 80:
                objetivo = "💪"
            elif porcentaje > 80 and porcentaje < 100:
                objetivo = "🚀"
            else:
                objetivo = "💯"
            
            horas_totales = segundos_totales / 3600     

            linea = f"{emoticono_categoria} {tipo['habito']} -> {horas_string_a_HHMM(horas_totales)}/{tipo['objetivo']} horas ({porcentaje:.2f}%) {objetivo}"
            lineas.append(linea)

        return lineas

def categorias_est(habitos, temporizadores, categorias):
    
        ahora = datetime.now()
        lineas = []
        
        for categoria in categorias:
            segundos_totales = 0
            for habito in habitos:
                if habito['id_categoria'] == categoria['id']:
                   # objetivo += int(habito['objetivo'])
                    for temporizador in temporizadores:
                        if temporizador['id_habito'] == habito['id']:
                            segundos_totales += horas_a_segundos(temporizador['tiempo'])

            # Icono de la categoría (💪, 🎮, 📖)
            
            emoticono_categoria = categoria['emoticono']
          
          #  try:
           #     porcentaje = (float(segundos_totales) / (float(objetivo)* 3600)) * 100
           # except ZeroDivisionError:
            #    porcentaje = 0
            linea = f"{emoticono_categoria} {categoria['categoria']} -> {numero_string_a_HHMM(segundos_totales)} horas"
            lineas.append(linea)

        return lineas

def categorias_fecha(habitos, temporizadores, categorias, tipo):
    
        lineas = []

        ahora = datetime.now().date()
        
        for categoria in categorias:
            segundos_totales = 0
            for habito in habitos:
                if habito['id_categoria'] == categoria['id']:
                   # objetivo += int(habito['objetivo'])
                    for temporizador in temporizadores:
                        if temporizador['id_habito'] == habito['id']:
                            if(cumple_periodo(temporizador['fecha'], ahora, tipo, 0)):
                                    segundos_totales += horas_a_segundos(temporizador['tiempo'])


            # Icono de la categoría (💪, 🎮, 📖)
            
            emoticono_categoria = categoria['emoticono']
          
          #  try:
           #     porcentaje = (float(segundos_totales) / (float(objetivo)* 3600)) * 100
           # except ZeroDivisionError:
            #    porcentaje = 0
            linea = f"{emoticono_categoria} {categoria['categoria']} -> {numero_string_a_HHMM(segundos_totales)} horas"
            lineas.append(linea)

        return lineas