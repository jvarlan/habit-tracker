import csv
from config import BASE_DIR
from .devolver import dev_nombre_habito_id
from .utilidades import print_color, print_color_pausa, cumple_periodo, numero_string_a_HHMM, ROJO, VERDE, CIAN, segundos_a_hhmmss, horas_a_segundos, horas_string_a_HHMM
from .mostrar import mostrar_csv_diccionario
from datetime import datetime, timedelta, date
from .checks import normalizar


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
    
def objetivos(tipos,temporizadores, tipo_periodo, offset):
        # saca los datos de los objetivos
        ahora = datetime.now()
        lineas = []
        for objetivo in tipos:
             
            id_habito = objetivo['id_habito']
            segundos_totales = 0

            habitos = mostrar_csv_diccionario("habitos")

            for habito in habitos:
                if habito['id'] == id_habito:
                    id_categoria = habito['id_categoria']
           

            categorias = mostrar_csv_diccionario("categorias")  
           
            for categoria in categorias:
                if categoria['id'] == id_categoria:
                    emoticono_categoria = categoria["emoticono"]
            
            for temporizador in temporizadores:
                if temporizador['id_habito'] == id_habito:
                    fecha_temp = datetime.strptime(temporizador['fecha'], "%Y-%m-%d").date()
                    if cumple_periodo(fecha_temp, ahora, tipo_periodo, offset):
                        segundos_totales = segundos_totales + horas_a_segundos(temporizador['tiempo'])         
            conseguido = ""
           
            if int(segundos_totales) >= int(horas_a_segundos(objetivo['objetivo'])):
                conseguido = "✔️"
            else:
                conseguido = "❌"
            habito = dev_nombre_habito_id(objetivo['id_habito'])
            linea = f"{emoticono_categoria} {habito} -> {numero_string_a_HHMM(segundos_totales)}/{objetivo['objetivo']} horas {conseguido}"
            lineas.append(linea)

        return lineas
def media_objetivos(tipos,temporizadores, tipo_periodo, num_periodos):
        # calcula la media dependiendo del tipo de periodo que sea (diario, semanal, mensual, anual)
        ahora = datetime.now()
        lineas = []
        for objetivo in tipos:     
            id_habito = objetivo['id_habito']
            segundos_totales = 0
            habitos = mostrar_csv_diccionario("habitos")

            for habito in habitos:
                if habito['id'] == id_habito:
                    id_categoria = habito['id_categoria']
           

            categorias = mostrar_csv_diccionario("categorias")  
            for categoria in categorias:
                if categoria['id'] == id_categoria:
                    emoticono_categoria = categoria["emoticono"]
            
            for offset in range(num_periodos):
                for temporizador in temporizadores:
                    if temporizador['id_habito'] == id_habito:
                        fecha_temp = datetime.strptime(temporizador['fecha'], "%Y-%m-%d")
                        if cumple_periodo(fecha_temp, ahora, tipo_periodo, offset):
                            segundos_totales = segundos_totales + horas_a_segundos(temporizador['tiempo'])
            conseguido = ""
            segundos_totales = segundos_totales / num_periodos
            if int(segundos_totales) >= int(horas_a_segundos(objetivo['objetivo'])) * 3600:
                conseguido = "✔️"
            else:
                conseguido = "❌"
            habito = dev_nombre_habito_id(objetivo['id_habito'])
            linea = f"{emoticono_categoria} {habito} -> {numero_string_a_HHMM(segundos_totales)}/{objetivo['objetivo']} horas {conseguido}"
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

def generar_bloque_resumen(titulo,objetivos,temporizadores,tipo, categorias, habitos):

    if not objetivos:
        print_color(f"No hay objetivos {titulo}",ROJO)
        return []
    return [
        print_color_pausa(f"\n{titulo}",VERDE),
        print_color_pausa("────────────────────────",VERDE),
        *resumen_est(objetivos, categorias, temporizadores, tipo, habitos, 0),
    ]

def resumen_est(objetivos, categorias, temporizadores, tipo_periodo, habitos, offset=0):
       
        ahora = datetime.now().date()
        lineas = []
        
        for objetivo in objetivos:     
            id_habito = objetivo['id_habito']
            for temporizador in temporizadores:
                
                if temporizador['id_habito'] == id_habito:
                    fecha_temp = datetime.strptime(temporizador['fecha'], "%Y-%m-%d").date()
                    segundos_totales = 0
                    if cumple_periodo(fecha_temp, ahora, tipo_periodo, offset):
                        segundos_totales = segundos_totales + horas_a_segundos(temporizador['tiempo'])
            

            # Icono de la categoría (💪, 🎮, 📖)
            
            id_habito_obj = int(objetivo["id_habito"])
            id_categoria_habito = None
            contador = 0
            for habito in habitos:
                contador +=1
                if habito['id'] == objetivo['id_habito']:
                    id_categoria_habito = habito['id_categoria']
                    break
            try:
                for categoria in categorias:
                    if id_categoria_habito == categoria['id']:
                        emoticono_categoria = categoria['emoticono']
            except IndexError:
                emoticono_categoria = "❓"
            
            try:
                porcentaje = (float(segundos_totales) / (float(horas_a_segundos(objetivo['objetivo'])))) * 100
            except NameError:
                segundos_totales = 0
                porcentaje = (float(segundos_totales) / (float(horas_a_segundos(objetivo['objetivo'])))) * 100


            if porcentaje == 0:
                emoti_objetivo = "👎"
            elif porcentaje > 0 and porcentaje <= 50:
                emoti_objetivo = "📈"
            elif porcentaje > 50 and porcentaje <= 80:
                emoti_objetivo = "💪"
            elif porcentaje > 80 and porcentaje < 100:
                emoti_objetivo = "🚀"
            else:
                emoti_objetivo = "💯"
         
            horas_totales = segundos_totales / 3600     
            
            linea = f"{emoticono_categoria} {habito['habito']} -> {horas_string_a_HHMM(horas_totales)}/{objetivo['objetivo']} horas ({porcentaje:.2f}%) {emoti_objetivo}"
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

def preparar_datos_estadistica(temporizadores, habitos, categorias):
    
    habitos_dict = {h['id']: h for h in habitos}
    categorias_dict = {c['id']: c for c in categorias}

    horas_totales = 0
    fechas = []
    horas_por_fecha = {}

    for t in temporizadores:   
        h = habitos_dict.get(t['id_habito'])
    
        if not h:
            continue
           
        c = categorias_dict.get(h['id_categoria'])

        if not c:
            continue
        
        fecha = datetime.strptime(t['fecha'], "%Y-%m-%d").date()
        tiempo_segundos = horas_a_segundos(t['tiempo'])
        horas_totales += tiempo_segundos
        fechas.append(fecha)

        if fecha not in horas_por_fecha:
            horas_por_fecha[fecha] = 0
        horas_por_fecha[fecha] += tiempo_segundos


    return {
            "horas_totales": horas_totales,
            "fechas": fechas,
            "horas_por_fecha": horas_por_fecha
        }

def preparar_datos_habitos(temporizadores, habitos, categorias):
    
    habitos_dict = {h['id']: h for h in habitos}
    categorias_dict = {c['id']: c for c in categorias}

    horas_totales = 0
    fechas = []
    horas_por_fecha = {}
    habitos_datos = {}

    for t in temporizadores:   
        h = habitos_dict.get(t['id_habito'])

        if not h:
            continue
           
        c = categorias_dict.get(h['id_categoria'])

        if not c:
            continue
        
        fecha = datetime.strptime(t['fecha'], "%Y-%m-%d").date()
        tiempo_segundos = horas_a_segundos(t['tiempo'])
        horas_totales += tiempo_segundos
        fechas.append(fecha)

        if fecha not in horas_por_fecha:
            horas_por_fecha[fecha] = 0
        horas_por_fecha[fecha] += tiempo_segundos

        if h['id_habito'] not in habitos_datos:
            habitos_datos[h['id_habito']].append(fechas, horas_totales, horas_por_fecha)

    return {
            "horas_totales": horas_totales,
            "fechas": fechas,
            "horas_por_fecha": horas_por_fecha
        }


def calcular_estadisticas_globales(datos):
    hoy = date.today()
    fechas = sorted(set(datos["fechas"]))
    horas_totales = datos["horas_totales"]
    horas_por_fecha = datos["horas_por_fecha"]

    fecha_max = None
    horas_max = 0

    for fecha, horas in horas_por_fecha.items():
        if horas > horas_max:
            horas_max = horas
            fecha_max = fecha
    
    media_horas = horas_totales / len(fechas)

    racha_max = calcular_racha_maxima(fechas)
    racha_actual = calcular_racha_actual(fechas)

    dias_activos = len(fechas)
    primera_fecha = min(fechas)
    ultima_fecha = max(fechas)
    dias_totales = ((hoy - primera_fecha).days) + 1

    porcentaje_actividad = (dias_activos / dias_totales) * 100

    return {

        "horas_totales": segundos_a_hhmmss(horas_totales),

        "media_horas": segundos_a_hhmmss(media_horas),

        "fecha_max": fecha_max,

        "record_horas_dia": segundos_a_hhmmss(horas_max),

        "racha_max": racha_max,

        "racha_actual": racha_actual,

        "dias_activos": dias_activos,

        "dias_totales": dias_totales,

        "porcentaje_actividad": round(porcentaje_actividad, 2),

        "primera_fecha": primera_fecha,

        "ultima_fecha": ultima_fecha
    }

def calcular_racha_maxima(fechas):
    if not fechas:
        return 0
    
    racha_max = 1
    racha_temp = 1

    for i in range(1, len(fechas)):
        diferencia = fechas[i] - fechas[i-1]

        if diferencia == timedelta(days=1):
            racha_temp += 1
        else:
            racha_max = max(racha_max, racha_temp)
            racha_temp = 1
   
    return max(racha_max, racha_temp)

def calcular_racha_actual(fechas):

    if not fechas:
        return 0
    fechas_set = set(fechas)

    hoy = date.today()

    if hoy not in fechas_set:
        return 0
    racha_actual = 1
    dia = hoy

    while(dia - timedelta(days=1)) in fechas_set:
        racha_actual += 1
        dia -= timedelta(days=1)
    return racha_actual

def mostrar_estadisticas_globales(stats):


    print("\n=== RESUMEN GLOBAL ===\n")

    print(f"Total de horas registradas: {stats['horas_totales']}")

    print(f"Media de los registros: {stats['media_horas']}\n")

    print(f"Primer registro: {stats['primera_fecha']}")

    print(f"Último registro: {stats['ultima_fecha']}\n")

    print(
        f"Días activos: "
        f"{stats['dias_activos']} / {stats['dias_totales']} "
        f"({stats['porcentaje_actividad']}%)"
    )

    print(
        f"Día más productivo: "
        f"{stats['fecha_max']} "
        f"({stats['record_horas_dia']})"
    )

    print("\n=== CONSTANCIA ===\n")

    print(f"Racha máxima: {stats['racha_max']}")

    print(f"Racha actual: {stats['racha_actual']}")