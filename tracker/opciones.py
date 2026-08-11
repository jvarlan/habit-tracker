from .utilidades import ROJO, VERDE, CIAN, GRIS, INVERSION, RESET, print_color, input_color, preguntar_seguir, print_color_pausa, limpiar_pantalla, imprimir_con_pausa, volver_atras, agrupar_datos_csv, cronometro, horas_a_segundos, segundos_a_hhmmss, muestra_habitos_registrados, normalizar
from .checks import comprobar_horas_temp,comprobar_horas_temp_24, validar_horas
from .guardar import registrar, registrar_categoria, habito, registrar_objetivo
from .mostrar import mostrar_registros, mostrar_temporizadores, mostrar_categorias, mostrar_csv, mostrar_csv_diccionario, mostrar_objetivos
from .devolver import dev_categoria_id, dev_categoria_correcta, dev_habito_id, dev_nombre_habito_id, dev_nombre_categoria_id, dev_id_categoria_habito_id, dev_emoticono_categoria_id
from .inputs import pedir_nombre_temp, pedir_horas_temp, pedir_fecha_temp, pedir_nombre_registro, pedir_objetivo_borrar, pedir_categoria_borrar, pedir_temporizador_borrar, pedir_habito_borrar, pedir_habito_modi, pedir_tempo_modi, pedir_categoria_modi, otro_objetivo, pedir_objetivo_modi
from .borrar import borrar_csv, borrar_temporizador, borrar_objetivo
from .fusion import fusionar_habitos, fusionar_objetivos, fusionar_temporizadores
from .estadisticas import generar_bloque_objetivo, generar_bloque_resumen, generar_bloque_categorias, calcular_estadisticas_globales, mostrar_estadisticas_globales, preparar_datos_estadistica, preparar_datos_habitos, calcular_estadisticas_habitos, mostrar_estadisticas_habitos, categorias_fecha, mostrar_mas_categorias
from datetime import datetime, date, timedelta
import emoji


volver = f"\n[ENTER] Salir"
volver2 = f"............................................................................"

def opcion_registro():

    while True:

            nombre = pedir_nombre_registro(volver)
            
            # da la opción de introducir volver y salir en todas sus variables
            if normalizar(nombre) in ("volver","salir",""):
                return False
            
            categorias = mostrar_csv_diccionario("categorias")
            cat_dict = {cat["categoria"]: cat["emoticono"] for cat in categorias}
            
            categorias_lista = sorted(cat_dict.keys())
            if categorias_lista:
                # si no está registrado, prosigue con el resto de inputs
                limpiar_pantalla()
                print_color(f"\nNuevo registro de hábito",INVERSION,"\n")
                print("\nCategorías disponibles:\n")
                
                for i, cat in enumerate(categorias_lista, 1):
                    print(f"{i}. {cat} {cat_dict[cat]}")

                categoria = input("\nIntroduce una categoria de la lista o añade una nueva: ")
                categoria_real = dev_categoria_correcta(categoria)
            else:
                categoria = input("Categoría: ")
                categoria_real = categoria
           
            if categoria_real in cat_dict:
                emoticono = cat_dict[categoria_real]
            else:
                emoticono = input("Introduce un emoticono asociado: ")
                while True:
                    if not emoji.is_emoji(emoticono):
                        emoticono = input_color("\nDebes introducir un único emoji: ",ROJO)
                        continue

                    if emoticono in cat_dict.values():
                        emoticono = input_color("\nEse emoji ya está en uso: ",ROJO)
                        continue
                    break
            lista_tipos = ["diario","semanal","mensual","anual"]
            opciones = ", ".join(lista_tipos[:-1]) + f" o {lista_tipos[-1]}"
                
            tipo = input(f"Elige un tipo de objetivo ({opciones}): ")
            while True:
                if normalizar(tipo) not in lista_tipos:
                    tipo = input_color("\nTipo de objetivo no válido. Introduce uno del paréntesis: ",ROJO)
                    continue
                break
                    
            objetivo = input(f"Objetivo (horas): ")
                
                # comprueba que las horas sean mayores que 0 y no contengan letras u otros caracteres
            while True:   
                if validar_horas(objetivo):
                    objetivo = validar_horas(objetivo)
                    registrar_categoria(categoria, emoticono)
                    id_categoria = dev_categoria_id(categoria)
                    id_habito = registrar(nombre, id_categoria)
                    registrar_objetivo(id_habito, tipo, objetivo)
                    print_color(f"\nHábito añadido correctamente.\n{nombre} | {categoria} {emoticono} | {tipo} | {objetivo} horas",VERDE,"\n")

                    otro_objetivo(id_habito, tipo, lista_tipos, nombre, categoria_real)
                else:
                    objetivo = input_color("\nEl objetivo debe ser un número mayor que 0. Introduce un valor válido: ",ROJO)
                    continue
                break

            seguir = input("\n¿Quieres introducir un nuevo hábito? s/n: ")
            lista = mostrar_registros()
            if preguntar_seguir(seguir):
                limpiar_pantalla()
                if not lista:
                    break
                continue
            else:
                break

def opcion_temporizador():
    lista = mostrar_temporizadores()
    while True: #empieza el bucle para seguir creando temporizadores
  
            lista = mostrar_csv_diccionario("habitos") # devuelve el listado de habitos registrados
            lista_minus = [item['habito'].lower() for item in lista] #crea una lista con los nombres de los habitos en minusculas para comparar con el input del usuario
            print_color(f"\nAñadir un nuevo temporizador",INVERSION,"\n")
            
            muestra_habitos_registrados(lista, volver)
            
            atributos_habito = pedir_nombre_temp(lista_minus,lista)
            if atributos_habito == None:
                return False
            while True:
                fecha = pedir_fecha_temp()  
                nombre = atributos_habito["habito"]
                id_habito = dev_habito_id(nombre)
                contador_horas_24 = comprobar_horas_temp_24(fecha, id_habito)
                if contador_horas_24 >= 24*3600:
                    print_color(f"Este temporizador ya tiene 24 horas registradas en este día.",ROJO)
                    continue
                while True:
                    horas = pedir_horas_temp()
                    id_habito = dev_habito_id(nombre)
                    contador_horas = comprobar_horas_temp(horas,fecha, id_habito)

                    if contador_horas > 24*3600:
                        print_color("El total de horas registradas para esta actividad no puede ser mayor de 24",ROJO)
                        continue #si la actividad supera las 24 horas el mismo día, vuelve a pedir las horas
                    else:     
                        habito(id_habito,horas,fecha)
                        fecha_formateada = fecha.strftime("%d/%m/%Y")
                        print_color(f"Tiempo registrado con éxito.\n{horas} | {nombre} | {fecha_formateada}",VERDE,"\n")
                        break # una vez es correcto, sale del bucle de horas y dias y vuelve al bucle original
                break
            seguir = input("\n¿Quieres introducir un nuevo temporizador? s/n: ")
            if preguntar_seguir(normalizar(seguir)):
                limpiar_pantalla()
                continue
            else:
                break    

def opcion_borrar():
    # muestra previamente todos los registros a eliminar
    lista = mostrar_csv_diccionario("habitos")
    if lista:
        while True:
            lista = mostrar_csv_diccionario("habitos")
            
            print_color(f"\nEliminar un hábito",INVERSION,"\n")
            muestra_habitos_registrados(lista, volver)
            borrar = pedir_habito_borrar()
            if borrar == None:
                break
            if borrar == "preguntar":
                lista = mostrar_csv_diccionario("habitos")

                if not lista:
                    break

                seguir = input("¿Quieres eliminar otro hábito? s/n: ")

                if preguntar_seguir(normalizar(seguir)):
                    limpiar_pantalla()
                    continue
                else:
                    break

            else:
                break
    else:
        print_color("No existe ningún hábito a eliminar.",CIAN)

def opcion_borrar_obj():
    # muestra previamente todos los registros a eliminar
    lista = mostrar_objetivos()

    if lista:
        while True:
            lista = mostrar_objetivos()
            #dev_habito_id
            #obtener_nombre_idhabito = id_habito_nombre()
            habitos = {}

            for i, item in enumerate(lista, start=1):
                
                id_habito = item["id_habito"]
                id_categoria = dev_id_categoria_habito_id(id_habito)
                emoticono = dev_emoticono_categoria_id(id_categoria)

                nombre = dev_nombre_habito_id(id_habito)

                if nombre not in habitos:
                    habitos[nombre] = {
                        "emoticono": emoticono,
                        "objetivos": []
                    }
                habitos[nombre]["objetivos"].append(
                    f"{i} - {item["tipo"]} - {item["objetivo"]} horas"
                    )
            print_color(f"\nEliminar un objetivo",INVERSION,"\n")
            print("\nLista de objetivos por hábito: \n")
            for nombre, info in sorted(habitos.items()):
                print(f"{nombre} {info['emoticono']}")
                print("─────────────────────────────")
                print(f"{'ID':<3} {'TIPO':>3} {'OBJETIVO':>13}")
                print("─────────────────────────────")
                for objetivo in info['objetivos']:
                    id, tipo, tiempo = [x.strip() for x in objetivo.split(" - ")]
                    print(
                        f"{id:<4}" 
                        f"{tipo.capitalize():<10}" 
                        f"{tiempo}"
                        )
                print()
            
            print_color(volver,CIAN)

            borrar = pedir_objetivo_borrar()
            
            if borrar == None:
                return False
            else:
                seguro = input(
                    f"{ROJO}"
                    f"\n¿Estás seguro de que quieres borrar el objetivo {borrar['tipo']}?{RESET}"
                    f"\n\nObjetivo: {borrar['objetivo']} horas"
                    f"\nHábito: {dev_nombre_habito_id(borrar['id_habito'])}"
                    f"\n\n{ROJO}Esta acción ELIMINARÁ el objetivo de forma PERMANENTE.{RESET}"
                    f"\n¿Confirmar? (s/n): {RESET}"
                )


                seguro = seguro.lower()

                if preguntar_seguir(normalizar(seguro)):
                    borrar_objetivo(borrar["id"],borrar)
                    print_color(f"\nObjetivo eliminado con éxito.",VERDE,"\n")
                else:
                    limpiar_pantalla()
                    continue

            lista = mostrar_objetivos()
            if lista:
                seguir = input("\n¿Quieres eliminar otro objetivo? s/n: ")
                if preguntar_seguir(normalizar(seguir)):
                    limpiar_pantalla()
                    continue
                else:
                    break    
    else:
        print_color("No existe ningún objetivo a eliminar.",CIAN)


def opcion_borrar_tempo():
    # muestra previamente todos los registros a eliminar
    lista = mostrar_temporizadores()

    if lista:     
        while True:
            habitos = {}
            for i, item in enumerate(lista, start=1):
                id_habito = item['id_habito']
                id_categoria = dev_id_categoria_habito_id(id_habito)
                emoticono = dev_emoticono_categoria_id(id_categoria)

                nombre = dev_nombre_habito_id(id_habito)
                
                if nombre not in habitos:
                    habitos[nombre] = {
                        "emoticono": emoticono,
                        "temporizadores": []
                    }
                habitos[nombre]["temporizadores"].append(
                    f"{i} - {item["fecha"]} - {item["horas"]}"
                )
            
            print_color(f"\nEliminar un temporizador",INVERSION,"\n")
            print("\nLista de temporizadores por hábito: \n")
            for nombre, info in sorted(habitos.items()):
                print(f"{nombre} {info['emoticono']}")
                print("───────────────────────────")
                print(f"{'ID':<3} {'FECHA':>3} {'HORAS':>13}")
                print("───────────────────────────")
                for temporizador in info['temporizadores']:
                    id, fecha, tiempo = [x.strip() for x in temporizador.split(" - ")]
                    fecha_formateada = datetime.strptime(fecha, "%Y-%m-%d").strftime("%d/%m/%Y")
                    print(
                        f"{id:<4}"
                        f"{fecha_formateada:<14}"
                        f"{tiempo}"
                    )
                print()
            
            print_color(volver,CIAN)
            borrar = pedir_temporizador_borrar()
            
            if borrar == None:
                return False
            else:
                seguro = input(
                    f'\n{ROJO}¿Quieres eliminar el temporizador '
                    f'{dev_nombre_habito_id(borrar["id_habito"])}?\n\n{RESET}'
                    f'Tiempo registrado: {borrar["horas"]}\n'
                    f'Fecha: {borrar["fecha"]}\n\n'
                    f'{ROJO}Esta acción no se puede deshacer.\n'
                    f'¿Confirmar? (s/n): {RESET}'
                )
                seguro = seguro.lower()
                if preguntar_seguir(normalizar(seguro)):
                    borrar_temporizador(borrar["id"],borrar)
                    print_color(f"\nTemporizador eliminado con éxito.",VERDE,"\n\n")
                else:
                    limpiar_pantalla()
                    continue
               
            lista = mostrar_temporizadores()
            if lista:
                seguir = input("\n¿Quieres eliminar otro temporizador? s/n: ")
                while True:
                    if preguntar_seguir(normalizar(seguir)):
                        limpiar_pantalla()
                        continue
                    else:
                        limpiar_pantalla()
                        break    
            else:
                break

    else:
        print_color("No existe ningún temporizador a eliminar.",CIAN)

def opcion_borrar_categoria():
    # muestra previamente todos los registros a eliminar
    while True:
        lista = mostrar_csv_diccionario("categorias")

        if lista:
        
            print_color(f"\nEliminar una categoría",INVERSION,"\n\n")
            print("Lista de categorías:\n")
            lista = sorted(lista, key=lambda x: x["categoria"])

            for i, item in enumerate(lista,start=1):
                print(f"{i} - {item['categoria']} {item['emoticono']}")
            print_color(volver,CIAN)
            borrar = pedir_categoria_borrar()
            if borrar is None:
                return False
            elif borrar is True:
                lista = mostrar_categorias()
                if not lista:
                    break
                
                seguir = input("\n¿Quieres eliminar otra categoría? s/n: ")
                if preguntar_seguir(normalizar(seguir)):
                    limpiar_pantalla()
                    continue
                else:
                    break    
            else:
                continue
    else:
        print_color("No existe ninguna categoria a eliminar.",CIAN)

def opcion_borrar_todo():
    lista1 = mostrar_csv("habitos")
    lista2 = mostrar_csv("temporizadores")
    lista3 = mostrar_csv("categorias")
    lista4 = mostrar_csv("objetivos")


    if lista1 or lista2 or lista3 or lista4:
        seguro = input(f"\n{ROJO}¿Estás seguro de que quieres borrar todos los registros? s/n:{RESET} ")

        seguro = seguro.lower()

        if preguntar_seguir(normalizar(seguro)):
            borrar_csv("categorias.csv")
            borrar_csv("habitos.csv")
            borrar_csv("temporizadores.csv")
            borrar_csv("objetivos.csv")
            print(f"{VERDE}Todos los registros han sido eliminados.{RESET}")
        else:
            limpiar_pantalla()
            return
    else:
        print_color("No existen elementos a eliminar.",CIAN)

def opcion_modi_habito():
    # muestra previamente todos los registros a eliminar
    lista = mostrar_registros()

    if lista:
        while True:
            habitos_dict = mostrar_csv_diccionario("habitos")
            lista_objetivos = mostrar_csv_diccionario("objetivos")
            #ordena la lista por nombre (el segundo campo del csv)
            
            lista_objetivos = sorted(lista_objetivos, key=lambda x: x["id_habito"])
            
            habitos_dict = sorted(habitos_dict, key=lambda x: x["habito"])
            print_color(f"\nModificar un hábito",INVERSION,"\n")
            print("\nHábitos registrados: \n")

            for habito in sorted(habitos_dict, key=lambda x: x["habito"]):
                nombre = habito["habito"]
                emoticono = dev_emoticono_categoria_id(habito['id_categoria'])
                print(f"{nombre} {emoticono}")
                print("───────────────────────────")
               
                print(f"{'CATEGORÍA':>3} {'Nº OBJETIVOS':>13}")
                print("───────────────────────────")
                
                categoria = dev_nombre_categoria_id(habito['id_categoria'])
                numero_objetivos = len([o for o in lista_objetivos if o["id_habito"] == habito["id"]])
                print(
                    f"{categoria:<14}"
                    f"{numero_objetivos}"
                        )
                print()

            print_color(volver, CIAN)
            
            modificar = pedir_habito_modi()
           
            if modificar == "":
                break
            lista = mostrar_registros()
            if lista:
                seguir = input("\n¿Quieres modificar otro hábito? s/n: ")
                if preguntar_seguir(normalizar(seguir)):
                    limpiar_pantalla()
                    continue
                else:
                    break    
            else:
                break
    else:
        print_color("No existe ningún hábito a modificar.",CIAN)

def opcion_modi_tempo():
   
    # muestra previamente todos los registros a eliminar
    lista = mostrar_registros()

    if lista:
        while True:
            lista_todo = mostrar_csv("temporizadores")
            #ordena la lista por fecha (el tercer campo del csv)
            lista_todo = sorted(lista_todo, key=lambda x: x[3])

            print_color(f"\nModificar un temporizador",INVERSION,"\n")
            print("\nTemporizadores registrados: \n")
            print(f"{'Nº':<4} {'Fecha':<12} {'Tiempo':<12} {'Hábito'}")
            print("─────────────────────────────────────────────────")            
            for i, item in enumerate(lista_todo, start=1):
                temporizador = dev_nombre_habito_id(item[1])
                tiempo = item[2]
                fecha = item[3]
                print(f"{i:<4} {fecha:<12} {tiempo:<12} {temporizador}")
            print("─────────────────────────────────────────────────")

            print_color(volver, CIAN)
            
            modificar = pedir_tempo_modi(lista_todo)
           
            if modificar == "":
                break
            lista = mostrar_registros()
            if lista:
                seguir = input("\n¿Quieres modificar otro temporizador? s/n: ")
                if preguntar_seguir(normalizar(seguir)):
                    limpiar_pantalla()
                    continue
                else:
                    break    
            else:
                break
    else:
        print_color("No existe ningún temporizador a modificar.",CIAN)

def opcion_modi_objetivo():
    
    # muestra previamente todos los registros a modificar
    lista = mostrar_registros()

    if lista:
        while True:
            lista_todo = mostrar_csv("objetivos")
            #ordena la lista por fecha (el tercer campo del csv)
            print_color(f"\nModificar un objetivo",INVERSION,"\n")
            print("\nObjetivos registrados \n")
            print(f"{'Nº':<4} {'Periodo':<12} {'Tiempo':<12} {'Hábito'}")
            print("─────────────────────────────────────────────────")

            for i, item in enumerate(lista_todo, start=1):
                habito = dev_nombre_habito_id(item[1])
                tipo = item[2]
                objetivo = item[3]
                print(f"{i:<4} {tipo.capitalize():<12} {objetivo:<12} {habito}")
            print("─────────────────────────────────────────────────"  )
            print_color(volver, CIAN)
            
            modificar = pedir_objetivo_modi(lista_todo)
           
            if modificar == "":
                break
            lista = mostrar_registros()
            if lista:
                seguir = input("\n¿Quieres modificar otro objetivo? s/n: ")
                if preguntar_seguir(normalizar(seguir)):
                    limpiar_pantalla()
                    continue
                else:
                    break    
            else:
                break
    else:
        print_color("No existe ningún objetivo a modificar.",CIAN)


def opcion_modi_categoria():
  
    lista = mostrar_categorias()

    if lista:
        while True:
            lista_todo = mostrar_csv_diccionario("categorias")


            lista_todo = sorted(lista_todo, key=lambda x: x["categoria"])
            print_color(f"\nModificar una categoria",INVERSION,"\n")

            print("\nCategorias registradas: \n")

            for i, item in enumerate(lista_todo, start=1):
                id_categoria = item["id"]
                categoria = item["categoria"]
                emoticono = item["emoticono"]
                print(f"{i} - {categoria} {emoticono}")

            print_color(volver, CIAN)

            modificar = pedir_categoria_modi(lista_todo)

            if modificar == "volver":
                break
            lista = mostrar_registros()
            
            if lista:
                seguir = input("¿Quieres modificar otra categoria? s/n: ")
                if preguntar_seguir(normalizar(seguir)):
                    limpiar_pantalla()
                    continue
                else:
                    break    
            else:
                break

def opcion_estadistica_objetivo():
    diarios, semanales, mensuales, anuales, habitos, temporizadores, categorias = agrupar_datos_csv()

    lineas = [
        print_color_pausa("=======================================", CIAN),
        print_color_pausa("  🎯  OBJETIVOS    ", CIAN),
        print_color_pausa("=======================================", CIAN),
        *generar_bloque_objetivo("Diarios", diarios, temporizadores, "dia", "Día", 7),
        *generar_bloque_objetivo("Semanales", semanales, temporizadores, "semana", "Semana", 4),
    ]
    
    imprimir_con_pausa(lineas)

    while True:
        texto_mensual = "[M] Mensuales"
        texto_anual = "[A] Anuales"
        if not mensuales:
            texto_mensual = f"{GRIS}[M] Mensuales{RESET}"
        if not anuales:
            texto_anual = f"{GRIS}[A] Anuales{RESET}"
        mostrar_mas = normalizar(input(
            f"\n{texto_mensual}   {texto_anual}   [ENTER] Salir: "
        ))

        if mostrar_mas in ("","volver","salir"):
            break
        if mostrar_mas == "m":
            if not mensuales:
                print_color(f"\nNo hay objetivos mensuales.",ROJO,"\n")
                continue
            else:
                lineas_mes = generar_bloque_objetivo("Mensuales", mensuales, temporizadores, "mes", "Mes", 4)
                imprimir_con_pausa(lineas_mes)
        elif mostrar_mas == "a":
            if not anuales:
                print_color(f"\nNo hay objetivos anuales.",ROJO,"\n")
                continue
            else:
                lineas_año = generar_bloque_objetivo("Anuales", anuales, temporizadores, "año", "Año", 4)
                imprimir_con_pausa(lineas_año)


def opcion_estadistica_resumen():
    salir = False
    while not salir:

        diarios, semanales, mensuales, anuales, habitos, temporizadores, categorias = agrupar_datos_csv()


        lineas = [
        print_color_pausa("\n=======================================",CIAN),
        print_color_pausa("  📊 RESUMEN DE HÁBITOS REGISTRADOS    ",CIAN),
        print_color_pausa("=======================================",CIAN),
        
        *generar_bloque_resumen("DIARIOS", diarios, temporizadores, "dia", categorias, habitos),
        *generar_bloque_resumen("SEMANALES", semanales, temporizadores, "semana", categorias, habitos),
    ]
        imprimir_con_pausa(lineas)

        while True:
            texto_mensuales = "[M] Mensuales"
            texto_anuales = "[A] Anuales"
            if not mensuales:
                texto_mensuales = f"{GRIS}[M] Mensuales{RESET}"
            if not anuales:
                texto_anuales = f"{GRIS}[A] Anuales{RESET}"
            mostrar_mas = normalizar(input(
                f"\n{texto_mensuales}   {texto_anuales}   [ENTER] Salir: "
            ))

            if mostrar_mas in ("","volver","salir"):
                salir = True  # Indicamos que queremos salir de todo
                break  # Salimos del bucle interno
            if mostrar_mas == "m":
                if not mensuales:
                    print_color("\nNo hay objetivos MENSUALES", ROJO,"\n")
                    continue
                else:
                    lineas_mes = generar_bloque_resumen("MENSUALES", mensuales, temporizadores, "mes",categorias, habitos)
                imprimir_con_pausa(lineas_mes)
            elif mostrar_mas == "a":
                if not anuales:
                    print_color("\nNo hay objetivos ANUALES", ROJO,"\n")
                    continue
                else:
                    lineas_año = generar_bloque_resumen("ANUALES", anuales, temporizadores, "año",categorias, habitos)
                imprimir_con_pausa(lineas_año)

def opcion_estadistica_categoria():
    mostrar_mas = False
    while not mostrar_mas:

        diarios, semanales, mensuales, anuales, habitos, temporizadores, categorias = agrupar_datos_csv()


        lineas = [
        print_color_pausa("\n=======================================",CIAN),
        print_color_pausa("  📊  CATEGORÍAS    ",CIAN),
        print_color_pausa("=======================================",CIAN),
        *generar_bloque_categorias(habitos, temporizadores, categorias),
           
    ]
        imprimir_con_pausa(lineas)
        
        lineas_mes, tiempo_mes = categorias_fecha(habitos, temporizadores, categorias, "mes")
        lineas_año, tiempo_año = categorias_fecha(habitos, temporizadores, categorias, "año")
        lineas_historico, tiempo_historico = categorias_fecha(habitos, temporizadores, categorias, "historico")
        resultado = mostrar_mas_categorias(lineas_mes, tiempo_mes, lineas_año, tiempo_año, lineas_historico, tiempo_historico)
        imprimir_con_pausa(resultado)


        if resultado == []:
            mostrar_mas = True

def opcion_estadistica_rachas():
    salir = False

    while not salir:

        temporizadores = mostrar_csv_diccionario("temporizadores")
        habitos = mostrar_csv_diccionario("habitos")
        categorias = mostrar_csv_diccionario("categorias")

        datos = preparar_datos_estadistica(temporizadores, habitos, categorias)
        estadisticas = calcular_estadisticas_globales(datos)
        
        mostrar_estadisticas_globales(estadisticas)
        
        salir = normalizar(input(
            "\n[ENTER] Salir: "
        ))

        if salir in ("","volver","salir"):
            salir = True

def opcion_estadistica_habitos():
    salir = False

    while not salir:
        temporizadores = mostrar_csv_diccionario("temporizadores")
        habitos = mostrar_csv_diccionario("habitos")
        categorias = mostrar_csv_diccionario("categorias")
 
        habitos_datos = preparar_datos_habitos(temporizadores, habitos, categorias)
        lineas = [
            print_color_pausa("=======================================", CIAN),
            print_color_pausa("  📋  HÁBITOS    ", CIAN),
            print_color_pausa("=======================================", CIAN),
              
        ]
            
        imprimir_con_pausa(lineas)

        datos_a_mostrar = []
        for nombre_habito, datos in habitos_datos.items():
            if not datos["fechas"]:
                continue

            estadisticas = calcular_estadisticas_habitos(datos, nombre_habito)

        
            datos_a_mostrar.extend(mostrar_estadisticas_habitos(estadisticas))

            

            horas_totales = datos['horas_totales']
            fechas = datos['fechas']
            horas_por_fecha = datos['horas_por_fecha']

        imprimir_con_pausa(datos_a_mostrar)

        salir = normalizar(input(
            f"\n{ROJO}[ENTER] Salir{RESET}"
        ))

        if salir in ("","volver","salir"):
            salir = True

def opcion_fusionar_habitos():
    
    lista = mostrar_csv_diccionario("habitos")

    if lista:
        print_color("Fusionar hábitos", INVERSION, "\n\n")
        for lista in lista:
            nombre = lista["habito"]
            id_categoria = lista["id_categoria"]
            emoticono = dev_emoticono_categoria_id(id_categoria)
            print(f"{nombre} {emoticono}")
        print_color("\nRecuerda que al fusionar hábitos, se combinarán los registros y objetivos de ambos hábitos en uno solo.", ROJO, "\n")
        print_color("\n[ENTER] para volver al menú de fusión.", CIAN, "\n")
        eleccion = input("\nElige los hábitos que quieres fusionar (separados por coma): ")
        while True:

            if eleccion.strip() == "":
                return
            elecciones = [h.strip() for h in eleccion.split(",")]
            if len(elecciones) != 2:
                
                eleccion = input(f"\n{ROJO}Debes seleccionar exactamente dos hábitos: {RESET}")
                continue
            else:
                break
            
        habito_1, habito_2 = elecciones

        id_habito_1 = dev_habito_id(habito_1)
        id_habito_2 = dev_habito_id(habito_2)

        habito_1 = dev_nombre_habito_id(id_habito_1)
        habito_2 = dev_nombre_habito_id(id_habito_2)

        if id_habito_1 and id_habito_2:
            # Fusionar los hábitos
            elige = input(f"¿Cuál de los dos hábitos quieres conservar como principal? {habito_1}/{habito_2}: ")
            id_principal = dev_habito_id(elige)
            id_secundario = id_habito_1 if id_principal == id_habito_2 else id_habito_2
            seguir = input(f"\n{ROJO}¿Estás seguro de que quieres fusionar '{habito_1}' y '{habito_2}'? Esta acción no se puede deshacer. (s/n): {RESET}")

            if preguntar_seguir(normalizar(seguir)):
                # Aquí puedes implementar la lógica para fusionar los hábitos seleccionados
                fusionar_habitos(id_principal, id_secundario)
                fusionar_objetivos(id_principal, id_secundario)
                fusionar_temporizadores(id_principal, id_secundario)
                print_color(f"\nLos hábitos '{habito_1}' y '{habito_2}' han sido fusionados correctamente.", VERDE, "\n")
                input("\n[ENTER] para continuar...")
            else:
                print_color("\nFusión cancelada.", ROJO, "\n")
                input("\n[ENTER] para continuar...")
    else:
        print_color(
            "Actualmente no existe ningún elemento a fusionar.",
            CIAN
        )

def opcion_fusionar_categorias():
    
    lista = mostrar_csv_diccionario("categorias")

    if lista:
        print_color("Fusionar categorías", INVERSION, "\n\n")
        for lista in lista:
            nombre = lista["categoria"]
            id_categoria = lista["id"]
            emoticono = dev_emoticono_categoria_id(id_categoria)
            print(f"{nombre} {emoticono}")
        print_color("\nRecuerda que al fusionar categorías, se combinarán los hábitos y registros de ambas categorías en una sola.", ROJO, "\n")
        print_color("\n[ENTER] para volver al menú de fusión.", CIAN, "\n")
        eleccion = input("\nElige las categorías que quieres fusionar (separadas por coma): ")
        if eleccion.strip() == "":
            return
        categoria_1, categoria2 = [c.strip() for c in eleccion.split(",")]
        id_categoria_1 = dev_categoria_id(categoria_1)
        id_categoria_2 = dev_categoria_id(categoria2)
        if id_categoria_1 and id_categoria_2:
            # Fusionar las categorías
            seguir = input(f"\n{ROJO}¿Estás seguro de que quieres fusionar '{categoria_1}' y '{categoria2}'? Esta acción no se puede deshacer. (s/n): {RESET}")
            if preguntar_seguir(normalizar(seguir)):
                # Aquí puedes implementar la lógica para fusionar las categorías seleccionadas
                print_color(f"\nLas categorías '{categoria_1}' y '{categoria2}' han sido fusionadas correctamente.", VERDE, "\n")
                input("\n[ENTER] para continuar...")
            else:
                print_color("\nFusión cancelada.", ROJO, "\n")
                input("\n[ENTER] para continuar...")
    else:
        print_color(
            "Actualmente no existe ningún elemento a fusionar.",
            CIAN
        )