from datetime import datetime
import time
import threading
import emoji
from .checks import normalizar, validar_horas, comprobar_horas_temp_24, comprobar_registro, validar_borrar_temporizador, comprobar_categoria
from .mostrar import mostrar_registros, mostrar_temporizadores, mostrar_categorias, mostrar_csv, mostrar_csv_diccionario, mostrar_objetivos
from .guardar import registrar_objetivo, registrar_categoria
from .contar import contar_csv_n, contar_csv_id
from .devolver import dev_habito_id, dev_habito_datos, dev_nombre_habito_id, dev_tipo_objetivo, dev_idhabito_temporizador, dev_lista_objetivos_cat, dev_categoria_id, dev_nombre_categoria_id, dev_lista_habitos_cat, dev_lista_temporizadores_cat, dev_emoticono_categoria_id, dev_habito_correcto, dev_categoria_correcta
from .borrar import borrar_temporizadores, borrar_habito, borrar_categoria, borrar_objetivos_id_habito
from .modificar import modificar_habito, modificar_temporizador, modificar_categoria, modificar_objetivo
from .utilidades import ROJO, VERDE, CIAN, AMARILLO, NARANJA, RESET, INVERSION, normalizar, print_color, input_color, cronometro, esperar_enter, horas_a_segundos, preguntar_seguir, limpiar_pantalla, muestra_habitos_registrados, muestra_habitos_registrados_color, obtener_emojis_sugeridos

def pedir_nombre_registro(volver):
    while True:
        diccionario = mostrar_csv_diccionario("habitos")
        print_color(f"\nNuevo registro de hábito",INVERSION,"\n")
        if diccionario:
            muestra_habitos_registrados_color(diccionario, volver)
            print_color("Añadir nuevo objetivo: introduce un nombre de la lista.",CIAN)
            nombre = input("Introduce el nombre del hábito: ")
        else:
            nombre = input("\nIntroduce el nombre del hábito: ")
       # limpiar_pantalla()

     # devuelve el número de veces que el nombre está registrado
        comprobado = comprobar_registro(normalizar(nombre))

        # si está registrado, vuelve a pedir el nombre
        if comprobado == 0:
            return nombre
        elif comprobado > 0:
            # aqui no deberia ahora obligar a repetir el nombre, ya que ahora se añadirán nuevos objetivos al introducir uno ya existente.

            datos_habito = dev_habito_datos(nombre)
            nombre_real = datos_habito['habito']
            id_habito = datos_habito['id']
            categoria = dev_nombre_categoria_id(datos_habito['id_categoria'])
            lista_tipos_usados = dev_tipo_objetivo(id_habito)
            lista_tipos = ['diario','semanal','mensual','anual']

            resultado = otro_objetivo(id_habito, lista_tipos_usados, lista_tipos, nombre_real, categoria)
            if resultado is False:
                return     
def pedir_tipo_habito():
    while True:
        lista_tipos = ["diario","semanal","mensual","anual"]
        tipo = input(f"Objetivo ({lista_tipos}): ")
        if normalizar(tipo) not in lista_tipos:
            continue
        break
    return lista_tipos, tipo
def pedir_nombre_temp(lista_minus,lista):
    nombre = input("Hábito a temporizar: ")
    while True:
        nombre = normalizar(nombre)

        for i, item in enumerate(lista_minus):
            if normalizar(item) == nombre:
                return lista[i]
        if normalizar(nombre) in ("volver","salir",""):
            return None
        else:
            nombre = input_color(f"\nIntroduce un temporizador de la lista: ",ROJO)

def pedir_horas_temp():
    registro = input("Pulsa 'M' para registro manual o 'A' para automático: ")
    while True:
        if registro.lower().strip() not in ("m", "a"):
            registro = input(f"{ROJO}\nOpción no válida. Pulsa 'M' para manual o 'A' para automático: {RESET}").lower().strip()
            continue
        if normalizar(registro) == "m":
            horas = input("Duración de la actividad (HH:MM:SS): ")
            while True:
                if validar_horas(horas):
                        horas = validar_horas(horas)
                        print()
                        return horas
                else:
                    horas = input_color(f"\nIntroduce un valor válido (HH:MM:SS): ",ROJO)
                    continue

        elif normalizar(registro) == "a":
            stop_event = threading.Event()
            resultado = []

            print_color("\n[ENTER] Parar el cronómetro ",CIAN)
            
            
            hilo_input = threading.Thread(target=esperar_enter, args=(stop_event,))
            hilo_input.start()

            hilo_crono = threading.Thread(target=cronometro, args=(stop_event, resultado))
            hilo_crono.start()

            hilo_crono.join()
            hilo_input.join()

            horas = resultado[0]
            if validar_horas(horas):
                return horas
        

def pedir_fecha_temp():
    
    fecha = input("Introduce la fecha (DD/MM/AAAA) o déjalo vacío para hoy: ")
    while True:       
        if fecha == "":
            fecha = datetime.now().date()
        else:
            try:
                fecha = datetime.strptime(fecha, "%d/%m/%Y").date()
                fecha_hoy = datetime.now().date()

                if fecha > fecha_hoy:
                    fecha = input(f"\n{ROJO}No puedes introducir una fecha superior a la actual. Introduce una válida: {RESET}")
                    continue
            except ValueError:
                fecha = input(f"\n{ROJO}Introduce una fecha válida (DD/MM/AAAA): {RESET}")
                continue
        return fecha
def pedir_habito_borrar():

    lista = mostrar_registros()
    if lista:
        borrar = input("Introduce el nombre del elemento a borrar: ")
        if normalizar(borrar) in ("volver","salir",""):
            return None
    while True:    
        borrar_id = dev_habito_id(borrar)
        temporizadores = contar_csv_n("temporizadores",borrar_id,0)
        objetivos = contar_csv_id("objetivos",borrar_id,1)
        habitos = contar_csv_n("habitos",borrar_id,0)
    
        if habitos == False:
            borrar = input_color("\nEste hábito no existe. Introduce uno de la lista: ",NARANJA)
            continue
        else:
            borrar = dev_habito_correcto(borrar)
            print(f"\nEl hábito {borrar} tiene {objetivos} objetivos y {temporizadores} registros de horas asociados.")
            print_color(f"⚠️  Esta acción borrará los DATOS de forma PERMANENTE.",ROJO)
            while True:
                seguro = input(f"{AMARILLO}¿Quieres continuar? s/n: {RESET}")
                seguro = seguro.lower()

                resultado = preguntar_seguir(seguro)
    
                if resultado is None:
                    print_color("❌ Valor inválido. Introduce 's' o 'n'.",CIAN)
                    continue
    
                if resultado is False:
                    return
            
                registros = borrar_temporizadores(borrar_id,temporizadores)
                habito = borrar_habito(borrar,borrar_id)
                borrar_objetivos_id_habito(borrar_id)
                print_color(f"\nEl hábito {borrar} se ha eliminado con éxito.",VERDE)
                return "preguntar"
        
def pedir_categoria_borrar():
    lista = mostrar_categorias()
    if lista:
        borrar = input("Introduce el nombre de la categoría a borrar: ")
        if normalizar(borrar) in ("volver","salir",""):
            return None
        
        while True:
            if comprobar_categoria(normalizar(borrar)) is True:
        
                id_categoria = dev_categoria_id(borrar)
                lista_habitos = dev_lista_habitos_cat(id_categoria)
                lista_objetivos_categoria = dev_lista_objetivos_cat(lista_habitos)
                lista_temporizadores = dev_lista_temporizadores_cat(lista_habitos)
                break
            else:
                borrar = input_color("\nOpción no válida. Introduce una categoría existente: ",ROJO)
                continue
               
        borrar = dev_categoria_correcta(borrar)

        print(
                f"\nLa categoría {borrar} contiene:\n"
                f"  • {len(lista_objetivos_categoria)} objetivos\n"
                f"  • {len(lista_habitos)} hábitos\n"
                f"  • {len(lista_temporizadores)} registros de tiempo\n",
            )

        print_color(
                "⚠️  Esta acción eliminará estos datos de forma PERMANENTE.",
                ROJO
            )

        seguro = input(f"{ROJO}¿Quieres continuar? (s/n): {RESET}")

        seguro = seguro.lower()
            
        if preguntar_seguir(normalizar(seguro)):
            habito = borrar_categoria(borrar,id_categoria,lista_habitos,lista_temporizadores, lista_objetivos_categoria)
            print_color(f"\nCategoría {borrar} y todos sus elementos han sido eliminados con éxito.\n {borrar} y todos sus elementos",VERDE,"\n")
            return True
        else:
            limpiar_pantalla()
            return "cancelar"
    else:
        return None

def pedir_objetivo_borrar():
    
        lista = mostrar_objetivos()
        if lista:
            borrar = input("Introduce el número del objetivo a borrar: ")
            if normalizar(borrar) in ("volver","salir",""):
                return None
            else:
                while True:    
                    borrar = validar_borrar_temporizador(borrar,lista)
                    if borrar is None:
                        borrar = input_color("\nDebes introducir un número válido: ", NARANJA)
                        continue
                    else:
                        return borrar
        else:
            return None


def pedir_temporizador_borrar():
    lista = mostrar_temporizadores()
    if lista:
        
        borrar = input("Introduce el número del temporizador a borrar: ")
        if normalizar(borrar) in ("volver","salir",""):
            return None
        else:
            while True:
                validado = validar_borrar_temporizador(borrar,lista)
                if validado is None:
                    borrar = input_color("\nDebes introducir un número válido: ", ROJO)
                    continue
                else:
                    return validado
    else:
        return None
        
def pedir_habito_modi():

    lista = mostrar_registros()

    if not lista:
        print_color(
            "\nNo hay hábitos registrados.",
            CIAN,
            "\n"
        )
        return ""

    habito_modificar = input(
        "Introduce el nombre del hábito a modificar: "
    )

    if normalizar(habito_modificar) in ("volver", "salir", ""):
        return ""

    while True:

        habitos = contar_csv_id(
            "habitos",
            dev_habito_id(habito_modificar),
            0
        )

        if habitos == False:

            habito_modificar = input_color(
                "\nEste hábito no existe. "
                "Introduce uno válido: ",
                ROJO
            )

            if normalizar(habito_modificar) in (
                "volver",
                "salir",
                ""
            ):
                return ""

            continue

        else:

            todo_habito = mostrar_csv_diccionario("habitos")

            for fila in todo_habito:

                if (
                    fila["habito"].lower()
                    == habito_modificar.lower()
                ):

                    habito = fila["habito"]

                    categoria = dev_nombre_categoria_id(
                        fila["id_categoria"]
                    )

                    break

            print_color(
                f"\nHábito actual: {habito}",
                CIAN
            )

            contadorh = 0
            contadorc = 0

            # -----------------------------------------
            # MODIFICAR NOMBRE
            # -----------------------------------------

            seguro = input(
                f"{NARANJA}"
                f"¿Quieres modificar el nombre del hábito "
                f"{habito}? s/n: "
                f"{RESET}"
            )

            seguro = seguro.lower()

            if preguntar_seguir(normalizar(seguro)):

                while True:

                    nuevo_habito = input(
                        "Modificar nombre: "
                    )

                    if normalizar(nuevo_habito) in (
                        "volver",
                        "salir",
                        ""
                    ):
                        nuevo_habito = habito
                        break

                    comprobado = comprobar_registro(
                        nuevo_habito
                    )

                    if comprobado > 0:

                        print_color(
                            "Este hábito ya está registrado. "
                            "Por favor, introduce uno nuevo.",
                            ROJO
                        )

                        continue

                    habito_modificar = nuevo_habito
                    contadorh += 1

                    break

            else:

                habito_modificar = habito

            # -----------------------------------------
            # MODIFICAR CATEGORÍA
            # -----------------------------------------

            seguro = input(
                f"{NARANJA}"
                f"\n¿Quieres modificar la categoría? s/n: "
                f"{RESET}"
            )

            seguro = seguro.lower()

            if preguntar_seguir(normalizar(seguro)):

                while True:

                    lista_todo = mostrar_csv_diccionario(
                        "categorias"
                    )

                    modificar_categoria = input(
                        "Modificar categoría: "
                    )

                    if normalizar(modificar_categoria) in (
                        "volver",
                        "salir",
                        ""
                    ):
                        modificar_categoria = categoria
                        id_categoria = dev_categoria_id(
                            modificar_categoria
                        )
                        break

                    # ---------------------------------
                    # CATEGORÍA YA EXISTENTE
                    # ---------------------------------

                    if any(
                        item.get("categoria")
                        == modificar_categoria
                        for item in lista_todo
                    ):

                        id_categoria = dev_categoria_id(
                            modificar_categoria
                        )

                        contadorc += 1

                        break

                    # ---------------------------------
                    # CATEGORÍA NUEVA
                    # ---------------------------------

                    else:

                        emojis_opcionales = [
                            "⭐",
                            "🌟",
                            "✨",
                            "🔥",
                            "💯",
                            "🎯",
                            "🏆",
                            "❤️",
                            "💚",
                            "💙",
                            "💜",
                            "🌱",
                            "🌿",
                            "☀️",
                            "🌙",
                            "🚀",
                            "💡",
                            "📌",
                            "⏰",
                            "✅",
                            "🎨",
                            "🎵",
                            "🎮",
                            "📚",
                            "💻",
                            "💰",
                            "🍎",
                            "🏠",
                            "🚗",
                            "✈️",
                            "🐶",
                            "🐱"
                        ]

                        categorias = (
                            mostrar_csv_diccionario(
                                "categorias"
                            )
                        )

                        cat_dict = {
                            cat["categoria"]:
                            cat["emoticono"]
                            for cat in categorias
                        }

                        # Emojis ya utilizados
                        emojis_usados = set(
                            cat_dict.values()
                        )

                        # Buscar sugerencias
                        emojis_sugeridos = (
                            obtener_emojis_sugeridos(
                                modificar_categoria
                            )
                        )

                        # Eliminar emojis ya utilizados
                        emojis_sugeridos = [
                            emoti
                            for emoti
                            in emojis_sugeridos
                            if emoti not in emojis_usados
                        ]

                        # Lista final
                        emojis_disponibles = (
                            emojis_sugeridos.copy()
                        )

                        # Completar hasta 7
                        for emoti in emojis_opcionales:

                            if len(
                                emojis_disponibles
                            ) >= 7:
                                break

                            if (
                                emoti not in emojis_usados
                                and
                                emoti
                                not in emojis_disponibles
                            ):

                                emojis_disponibles.append(
                                    emoti
                                )

                        print_color(
                            f"\nLa categoría "
                            f"{modificar_categoria} "
                            f"no existe. Se añadirá.",
                            CIAN
                        )

                        if emojis_sugeridos:

                            print(
                                "\nEmojis sugeridos "
                                "para esta categoría:\n"
                            )

                        else:

                            print(
                                "\nNo hay emojis específicos "
                                "para esta categoría.\n"
                            )

                        # ---------------------------------
                        # SELECCIONAR EMOJI
                        # ---------------------------------

                        while True:

                            for i, emoti in enumerate(
                                emojis_disponibles,
                                1
                            ):

                                print(
                                    f"{i}. {emoti}"
                                )

                            opcion_personalizada = (
                                len(
                                    emojis_disponibles
                                ) + 1
                            )

                            print(
                                f"{opcion_personalizada}. "
                                f"✏️  Personalizado"
                            )

                            opcion = input(
                                "\nSelecciona una opción: "
                            )

                            if opcion.isdigit():

                                opcion = int(opcion)

                                # -------------------------
                                # EMOJI DE LA LISTA
                                # -------------------------

                                if (
                                    1
                                    <= opcion
                                    <= len(
                                        emojis_disponibles
                                    )
                                ):

                                    emoticono = (
                                        emojis_disponibles[
                                            opcion - 1
                                        ]
                                    )

                                    break

                                # -------------------------
                                # EMOJI PERSONALIZADO
                                # -------------------------

                                elif (
                                    opcion
                                    == opcion_personalizada
                                ):

                                    while True:

                                        emoticono = input(
                                            "\nIntroduce tu "
                                            "propio emoji: "
                                        )

                                        if not emoji.is_emoji(
                                            emoticono
                                        ):

                                            input_color(
                                                "\nDebes introducir "
                                                "un único emoji. "
                                                "Pulsa Enter para "
                                                "continuar: ",
                                                ROJO
                                            )

                                            continue

                                        if (
                                            emoticono
                                            in emojis_usados
                                        ):

                                            input_color(
                                                "\nEse emoji ya "
                                                "está en uso. "
                                                "Pulsa Enter para "
                                                "continuar: ",
                                                ROJO
                                            )

                                            continue

                                        break

                                    break

                                else:

                                    input_color(
                                        "\nOpción no válida. "
                                        "Pulsa Enter para "
                                        "continuar: ",
                                        ROJO
                                    )

                            else:

                                input_color(
                                    "\nOpción no válida. "
                                    "Pulsa Enter para "
                                    "continuar: ",
                                    ROJO
                                )

                        # ---------------------------------
                        # REGISTRAR CATEGORÍA NUEVA
                        # ---------------------------------

                        registrar_categoria(
                            modificar_categoria,
                            emoticono
                        )

                        id_categoria = (
                            dev_categoria_id(
                                modificar_categoria
                            )
                        )

                        contadorc += 1

                        break

            else:

                modificar_categoria = categoria

                id_categoria = dev_categoria_id(
                    modificar_categoria
                )

            # -----------------------------------------
            # GUARDAR MODIFICACIONES
            # -----------------------------------------

            if contadorh > 0 and contadorc == 0:

                modificar_habito(
                    habito_modificar,
                    dev_habito_id(habito),
                    dev_categoria_id(
                        modificar_categoria
                    )
                )

                print_color(
                    f"\nEl hábito {habito} ha sido "
                    f"cambiado con éxito por "
                    f"{habito_modificar}.",
                    VERDE,
                    "\n"
                )

                break

            elif contadorh == 0 and contadorc > 0:

                modificar_habito(
                    habito_modificar,
                    dev_habito_id(habito),
                    dev_categoria_id(
                        modificar_categoria
                    )
                )

                print_color(
                    f"\nEl hábito {habito} ha sido "
                    f"cambiado con éxito a la categoría "
                    f"{modificar_categoria}.",
                    VERDE,
                    "\n"
                )

                break

            elif contadorh > 0 and contadorc > 0:

                modificar_habito(
                    habito_modificar,
                    dev_habito_id(habito),
                    dev_categoria_id(
                        modificar_categoria
                    )
                )

                print_color(
                    f"\nEl hábito {habito} ha sido "
                    f"cambiado con éxito por "
                    f"{habito_modificar} y a la categoría "
                    f"{modificar_categoria}.",
                    VERDE,
                    "\n"
                )

                break

            else:

                print_color(
                    "\nNo se ha modificado nada.",
                    CIAN,
                    "\n"
                )

                break

def pedir_tempo_modi(lista_todo):

    mensaje = "Introduce el número del temporizador a modificar: "

    while True:
        if lista_todo:
            try:
                modificar = input(mensaje)
                
                if normalizar(modificar) in ("volver","salir",""):
                    return ""
                modificar = int(modificar)

                if modificar <=0:
                    raise IndexError
                
                modificar = int(modificar)-1

                id_temporizador = lista_todo[modificar][0]
                temporizadores = contar_csv_id("temporizadores",id_temporizador,0)  

            except ValueError:
                mensaje = (f"{NARANJA}\nFormato incorrecto. Debes introducir un número de la lista: {RESET}")
                continue
            except IndexError:
                mensaje = (f"{ROJO}\nEste temporizador no existe. Debes introducir un número de la lista: {RESET}")
                continue

            todo_habito = mostrar_csv("temporizadores")
            todo_habito = sorted(todo_habito, key=lambda x: x[3])

            for fila in todo_habito:

                if fila[0] == id_temporizador:
                    habito = dev_nombre_habito_id(fila[1])
                    horas = fila[2]
                    fecha = fila[3]

            print_color(f"\nHábito actual: {habito}",CIAN,"\n")
            print_color(f"Hora actual: {horas}",CIAN,"\n")
            print_color(f"Fecha actual: {fecha} ",CIAN)

            contadorh = 0
            contadorf  = 0

            seguro = input(f"{AMARILLO}¿Quieres modificar las horas? s/n: {RESET}")
            seguro = seguro.lower()

            if preguntar_seguir(normalizar(seguro)):
                while True:
                    nueva_hora = pedir_horas_temp()
                    id_habito = lista_todo[modificar][1]
                
                    contador_horas_24 = comprobar_horas_temp_24(datetime.strptime(fecha, "%Y-%m-%d").date(), id_habito)
                    contador_horas_24_total = int(contador_horas_24) - int(horas_a_segundos(horas)) + int(horas_a_segundos(nueva_hora))

                
                    if contador_horas_24_total > 24 * 3600:
                        print_color(f"Este temporizador ya tiene 24 horas registradas en este día.",ROJO)
                        continue
                    else:
                        contadorh +=1
                        break
            else:
                nueva_hora = horas
            
            
            seguro = input(f"{AMARILLO}¿Quieres modificar la fecha del registro? s/n: {RESET}")
            seguro = seguro.lower()

            if preguntar_seguir(normalizar(seguro)):
                nueva_fecha = pedir_fecha_temp()
                contadorf +=1
            else:
                nueva_fecha = fecha
            
            if contadorh > 0 or contadorf > 0:

                modificar_temporizador(id_temporizador,nueva_hora,nueva_fecha)
                id_habito = dev_idhabito_temporizador(id_temporizador)
                print_color(f"\nSe ha actualizado el temporizador de {dev_nombre_habito_id(id_habito)}: {horas} horas ({fecha}) →  {nueva_hora} horas ({nueva_fecha}).",VERDE,"\n")
                return
            elif contadorh == 0 and contadorf == 0:
                print_color("\nNo se ha modificado nada.",CIAN,"\n")
                return
            elif contadorh > 0 and contadorf == 0:
                modificar_temporizador(id_temporizador,nueva_hora,nueva_fecha)
                id_habito = dev_idhabito_temporizador(id_temporizador)
                print_color(f"\nLas horas del temporizador {dev_nombre_habito_id(id_habito)} han cambiado de {horas} horas a {nueva_hora} horas ({nueva_fecha}).",VERDE,"\n")
                return
            elif contadorh == 0 and contadorf > 0:
                modificar_temporizador(id_temporizador,nueva_hora,nueva_fecha)
                id_habito = dev_idhabito_temporizador(id_temporizador)
                print_color(f"\nLa fecha del temporizador {dev_nombre_habito_id(id_habito)} ha cambiado de {fecha} a {nueva_fecha}.",VERDE,"\n")
                return
        

def pedir_objetivo_modi(lista_todo):
    mensaje = "Introduce el número del objetivo a modificar: "

    while True:
        if lista_todo:
            try:
                modificar = input(mensaje)
                
                if normalizar(modificar) in ("volver","salir",""):
                    return ""
                
                modificar = int(modificar) 

                if modificar <=0:
                    raise IndexError

                id_objetivo = lista_todo[modificar-1][0]            
                temporizadores = contar_csv_id("objetivos",id_objetivo,0)       

            except ValueError:
                mensaje = (f"{NARANJA}\nFormato incorrecto. Debes introducir un número de la lista: {RESET}")
                continue
            except IndexError:
                mensaje = (f"{ROJO}\nEste objetivo no existe. Debes introducir un número de la lista: {RESET}")
                continue

            lista_tipos_restantes = ["diario","semanal","mensual","anual"]
            todo_habito = mostrar_csv("objetivos")

            for fila in todo_habito:

                if fila[0] == id_objetivo:
                    id_habito = fila[1]
                    habito = dev_nombre_habito_id(fila[1])
                    tipo_objetivo = fila[2]
                    objetivo_horas = fila[3]

            for fila in todo_habito:        
                if fila[1] == id_habito:
                    lista_tipos_restantes.remove(fila[2])
           
            print_color(f"\nHábito actual: {habito}",CIAN,"\n")
            print_color(f"Periodo: {tipo_objetivo.capitalize()}",CIAN,"\n")
            print_color(f"Objetivo horas actual: {objetivo_horas} ",CIAN)

            contadorp = 0
            contadorh  = 0

            if not lista_tipos_restantes:
                print_color("No es posible cambiar el tipo de objetivo porque ya están ocupados.",ROJO)
                nuevo_objetivo = tipo_objetivo
            else:
                
                seguro = input(f"{AMARILLO}¿Quieres modificar el periodo? s/n: {RESET}")

                if preguntar_seguir(normalizar(seguro)):
                    if len(lista_tipos_restantes) == 1:
                        opciones = lista_tipos_restantes[0]
                    else:
                        opciones = ", ".join(lista_tipos_restantes[:-1]) + " o " + lista_tipos_restantes[-1]
                    nuevo_objetivo = input(f"Nuevo objetivo ({opciones}): ")
                    while True:
                        if nuevo_objetivo not in lista_tipos_restantes:
                            nuevo_objetivo = input_color(f"\nIntroduce un objetivo válido ({opciones}): ",ROJO)
                            continue
                        else:
                            contadorp +=1
                            break
                else:
                    nuevo_objetivo = tipo_objetivo  
                
            seguro = input(f"{AMARILLO}¿Quieres modificar las horas objetivo? s/n: {RESET}")

            if preguntar_seguir(normalizar(seguro)):
                objetivo = input("Objetivo (horas): ")
                while True:
                    # comprueba que las horas sean mayores que 0 y no contengan letras u otros caracteres  
                    if validar_horas(objetivo):
                        nueva_hora = validar_horas(objetivo)
                        contadorh +=1
                        break
                    else:
                        objetivo = input_color(f"\nIntroduce un valor válido (HH:MM:SS): ",ROJO)
                        continue
            else:
                nueva_hora = objetivo_horas
            if contadorp > 0 and contadorh > 0:    
                
                modificar_objetivo(id_objetivo,nuevo_objetivo,nueva_hora)
                id_habito = dev_idhabito_temporizador(id_objetivo)
                print_color(f"\nSe ha actualizado el objetivo de {habito}: {tipo_objetivo} ({objetivo_horas}) → {nuevo_objetivo} ({nueva_hora}).",VERDE,"\n")
                return
            elif contadorp == 0 and contadorh == 0:
                print_color("\nNo se ha modificado nada.",CIAN,"\n")
                return
            elif contadorp > 0 and contadorh == 0:
                modificar_objetivo(id_objetivo,nuevo_objetivo,nueva_hora)
                id_habito = dev_idhabito_temporizador(id_objetivo)
                print_color(f"\nEl periodo de {habito} ha cambiado de {tipo_objetivo} a {nuevo_objetivo}.",VERDE,"\n")
                return
            elif contadorp == 0 and contadorh > 0:
                modificar_objetivo(id_objetivo,nuevo_objetivo,nueva_hora)
                id_habito = dev_idhabito_temporizador(id_objetivo)
                print_color(f"\nEl objetivo de {habito} ha cambiado de {objetivo_horas} a {nueva_hora}.",VERDE,"\n")
                return
            


def pedir_categoria_modi(lista_todo):

    if not lista_todo:
        print_color(
            "\nNo hay categorías registradas.",
            CIAN,
            "\n"
        )
        return ""

    modificar = input(
        "Introduce el nombre de la categoría a modificar: "
    )

    if normalizar(modificar) in ("volver", "salir", ""):
        return "volver"

    categoria_encontrada = None

    while True:

        # -----------------------------------------
        # BUSCAR CATEGORÍA
        # -----------------------------------------

        categoria_encontrada = None

        for item in lista_todo:

            if (
                normalizar(item["categoria"])
                == normalizar(modificar)
            ):

                categoria_encontrada = item
                break

        if categoria_encontrada:

            categoria = categoria_encontrada["categoria"]
            emoticono = categoria_encontrada["emoticono"]
            id_categoria = categoria_encontrada["id"]

            break

        else:

            modificar = input_color(
                f"\nLa categoría {modificar} no existe. "
                f"Introduce una categoría válida: ",
                ROJO
            )

            if normalizar(modificar) in (
                "volver",
                "salir",
                ""
            ):
                return "volver"

    categorias = contar_csv_id(
        "categorias",
        id_categoria,
        0
    )

    # Contadores para saber qué se ha modificado
    contadorc = 0
    contadore = 0

    # -----------------------------------------
    # MODIFICAR NOMBRE
    # -----------------------------------------

    seguro = input(
        f"{AMARILLO}"
        f"¿Quieres modificar el nombre de la categoría? s/n: "
        f"{RESET}"
    )

    seguro = seguro.lower()

    if preguntar_seguir(normalizar(seguro)):

        while True:

            nueva_categoria = input(
                "Introduce el nuevo nombre para la categoría: "
            )

            if normalizar(nueva_categoria) in (
                "volver",
                "salir",
                ""
            ):

                nueva_categoria = categoria
                break

            # Comprobar que no sea el mismo nombre
            if (
                normalizar(nueva_categoria)
                == normalizar(categoria)
            ):

                nueva_categoria = input_color(
                    "\nNo puedes poner el mismo nombre. "
                    "Introduce otro: ",
                    ROJO
                )

                continue

            # Comprobar que no exista otra categoría
            categoria_repetida = any(
                normalizar(item["categoria"])
                == normalizar(nueva_categoria)
                and item["id"] != id_categoria
                for item in lista_todo
            )

            if categoria_repetida:

                nueva_categoria = input_color(
                    "\nEsa categoría ya existe. "
                    "Introduce otra: ",
                    ROJO
                )

                continue

            contadorc += 1
            break

    else:

        nueva_categoria = categoria

    # -----------------------------------------
    # MODIFICAR EMOJI
    # -----------------------------------------

    seguro = input(
        f"{AMARILLO}"
        f"\n¿Quieres modificar el emoticono asociado? s/n: "
        f"{RESET}"
    )

    seguro = seguro.lower()

    if preguntar_seguir(normalizar(seguro)):

        # Emojis generales para completar la lista
        emojis_opcionales = [
            "⭐",
            "🌟",
            "✨",
            "🔥",
            "💯",
            "🎯",
            "🏆",
            "❤️",
            "💚",
            "💙",
            "💜",
            "🌱",
            "🌿",
            "☀️",
            "🌙",
            "🚀",
            "💡",
            "📌",
            "⏰",
            "✅",
            "🎨",
            "🎵",
            "🎮",
            "📚",
            "💻",
            "💰",
            "🍎",
            "🏠",
            "🚗",
            "✈️",
            "🐶",
            "🐱"
        ]

        # -----------------------------------------
        # EMOJIS ACTUALMENTE USADOS
        # -----------------------------------------

        categorias = mostrar_csv_diccionario(
            "categorias"
        )

        # Excluir el emoji de la categoría actual,
        # porque el usuario podría querer mantenerlo
        emojis_usados = {
            item["emoticono"]
            for item in categorias
            if item["id"] != id_categoria
        }

        # -----------------------------------------
        # EMOJIS SUGERIDOS
        # -----------------------------------------

        emojis_sugeridos = obtener_emojis_sugeridos(
            nueva_categoria
        )

        # Eliminar emojis que ya estén utilizados
        emojis_sugeridos = [
            emoti
            for emoti in emojis_sugeridos
            if emoti not in emojis_usados
        ]

        # -----------------------------------------
        # LISTA FINAL DE EMOJIS
        # -----------------------------------------

        emojis_disponibles = (
            emojis_sugeridos.copy()
        )

        # Completar hasta 7 emojis
        for emoti in emojis_opcionales:

            if len(emojis_disponibles) >= 7:
                break

            if (
                emoti not in emojis_usados
                and emoti not in emojis_disponibles
            ):

                emojis_disponibles.append(
                    emoti
                )

        # -----------------------------------------
        # MOSTRAR EMOJIS
        # -----------------------------------------

        limpiar_pantalla()

        print_color(
            f"\nCategoría: {nueva_categoria}",
            CIAN,
            "\n"
        )

        if emojis_sugeridos:

            print(
                "Emojis sugeridos para esta categoría:\n"
            )

        else:

            print(
                "No hay emojis específicos "
                "para esta categoría.\n"
            )

        # -----------------------------------------
        # SELECCIONAR EMOJI
        # -----------------------------------------

        while True:

            for i, emoti in enumerate(
                emojis_disponibles,
                1
            ):

                print(
                    f"{i}. {emoti}"
                )

            opcion_personalizada = (
                len(emojis_disponibles) + 1
            )

            print(
                f"{opcion_personalizada}. "
                f"✏️  Personalizado"
            )

            opcion = input(
                "\nSelecciona una opción: "
            )

            if opcion.isdigit():

                opcion = int(opcion)

                # -----------------------------
                # EMOJI DE LA LISTA
                # -----------------------------

                if (
                    1
                    <= opcion
                    <= len(emojis_disponibles)
                ):

                    nuevo_emoticono = (
                        emojis_disponibles[
                            opcion - 1
                        ]
                    )

                    contadore += 1
                    break

                # -----------------------------
                # EMOJI PERSONALIZADO
                # -----------------------------

                elif (
                    opcion
                    == opcion_personalizada
                ):

                    while True:

                        nuevo_emoticono = input(
                            "\nIntroduce tu propio emoji: "
                        )

                        if not emoji.is_emoji(
                            nuevo_emoticono
                        ):

                            input_color(
                                "\nDebes introducir "
                                "un único emoji. "
                                "Pulsa Enter para continuar: ",
                                ROJO
                            )

                            continue

                        if (
                            nuevo_emoticono
                            in emojis_usados
                        ):

                            input_color(
                                "\nEse emoji ya está "
                                "en uso. "
                                "Pulsa Enter para continuar: ",
                                ROJO
                            )

                            continue

                        break

                    contadore += 1
                    break

                else:

                    input_color(
                        "\nOpción no válida. "
                        "Pulsa Enter para continuar: ",
                        ROJO
                    )

            else:

                input_color(
                    "\nOpción no válida. "
                    "Pulsa Enter para continuar: ",
                    ROJO
                )

    else:

        nuevo_emoticono = emoticono

    # -----------------------------------------
    # GUARDAR MODIFICACIONES
    # -----------------------------------------

    if categorias:

        if contadorc > 0 and contadore > 0:

            modificar_categoria(
                id_categoria,
                nueva_categoria,
                nuevo_emoticono
            )

            print_color(
                f"\nSe ha modificado la categoría "
                f"por {nueva_categoria} y el emoticono "
                f"asociado por {nuevo_emoticono}\n",
                VERDE,
                "\n"
            )

            return

        elif contadorc == 0 and contadore == 0:

            print_color(
                "\nNo se ha modificado nada.",
                CIAN,
                "\n\n"
            )

            return

        elif contadorc > 0 and contadore == 0:

            modificar_categoria(
                id_categoria,
                nueva_categoria,
                nuevo_emoticono
            )

            print_color(
                f"\nSe ha modificado la categoría "
                f"a {nueva_categoria}.",
                VERDE,
                "\n"
            )

            return

        elif contadorc == 0 and contadore > 0:

            modificar_categoria(
                id_categoria,
                nueva_categoria,
                nuevo_emoticono
            )

            print_color(
                f"\nEl emoticono asociado a la categoría "
                f"{nueva_categoria} se ha cambiado por "
                f"{nuevo_emoticono}.",
                VERDE,
                "\n"
            )

            return
                    
def otro_objetivo(id_habito, tipo, lista_tipos, nombre, categoria):
        
    lista_objetivos = mostrar_csv_diccionario("objetivos")
           
    tipos_usados = []

    for lista_o in lista_objetivos:
        if int(lista_o['id_habito']) == int(id_habito):
            tipo_o = lista_o.get('tipo')
            if isinstance(tipo_o, str) and tipo_o.strip():
                tipos_usados.append(tipo_o.strip().lower())
    
    if isinstance(tipo, list):
        for elemento in tipo:
            if isinstance(elemento, str):
                tipos_usados.append(elemento.strip().lower())
    else:
        if isinstance(tipo, str):
            tipos_usados.append(tipo.strip().lower())
    while True:
        
        tipos_restantes = [
            ltipos for ltipos in lista_tipos
            if isinstance(ltipos, str)
            and ltipos.strip().lower() not in tipos_usados
        ]
        if not tipos_restantes:
            input(f"{ROJO}\nEste hábito ya tiene todos los objetivos asignados. Pulsa ENTER para salir: {RESET}")
            limpiar_pantalla()
            return True
                
        otro_habito = input(f"\n¿Quieres añadir un objetivo diferente para {nombre}? s/n: ")
        
        resultado = preguntar_seguir(otro_habito)
        
        if resultado is None:
            print_color("❌ Valor inválido. Introduce 's' o 'n'.",CIAN)
            continue
        
        if resultado is False:
            return
        
        limpiar_pantalla()
               
        print_color(f"\nAsignación de objetivo para {nombre}",INVERSION,"\n\n")
        
        if len(tipos_restantes) > 1:
            opciones = ", ".join(tipos_restantes[:-1]) + " o " + tipos_restantes[-1]
        else:
            opciones = tipos_restantes[0]

        tipo_ad = normalizar(input(f"Elige un objetivo ({opciones}): "))
        while True:    
            if tipo_ad not in tipos_restantes:
                tipo_ad = input_color("\nTipo de objetivo no válido. Elige uno del paréntesis: ",ROJO)
                continue
            if normalizar(tipo_ad) in ("volver","salir"):
                limpiar_pantalla()
                return
            break

        objetivo_ad = input("Otro objetivo (horas): ")
        while True:
            if validar_horas(objetivo_ad):
                objetivo_ad = validar_horas(objetivo_ad)
                registrar_objetivo(id_habito, tipo_ad, objetivo_ad)
                print_color(f"\nObjetivo añadido con éxito.\n{nombre} | {tipo_ad} | {objetivo_ad} horas",VERDE,"\n")
                break
            else:
                objetivo_ad = input_color(f"\nIntroduce un valor válido (HH:MM:SS): ",ROJO)
                continue
    
        tipos_usados.append(tipo_ad.lower())        
