from .utilidades import ROJO, VERDE, CIAN, INVERSION, RESET, print_color, preguntar_seguir, print_color_pausa, limpiar_pantalla, imprimir_con_pausa, volver_atras, agrupar_datos_csv, cronometro
from .checks import comprobar_horas_temp,comprobar_horas_temp_24, normalizar, validar_horas
from .guardar import registrar, registrar_categoria, habito, registrar_objetivo
from .mostrar import mostrar_registros, mostrar_temporizadores, mostrar_categorias, mostrar_csv, mostrar_csv_diccionario
from .devolver import dev_categoria_id, dev_habito_id, dev_nombre_habito_id
from .inputs import pedir_nombre_temp, pedir_horas_temp, pedir_fecha_temp, pedir_nombre_registro, pedir_tipo_habito, pedir_categoria_borrar, pedir_temporizador_borrar, pedir_habito_borrar, pedir_habito_modi, pedir_tempo_modi, pedir_categoria_modi, otro_objetivo
from .borrar import borrar_csv, borrar_temporizador
from .estadisticas import generar_bloque_objetivo, generar_bloque_resumen, generar_bloque_categorias
from datetime import datetime

volver = f"\nPulsa 'ENTER' si quieres salir al menú de opciones."
volver2 = f"\n............................................................................"

def opcion_registro():

        while True:
            lista = mostrar_registros()
            print_color("\nRegistrar un nuevo hábito",INVERSION)
            if lista:
                print("\nHábitos registrados: \n")
                # recorre el listado, numerandolo con el nombre al lado
                for i, item in enumerate(sorted(lista, key=lambda x: x.strip().lower()), start=1):
                    print(f"👉 {item}")
            print_color(volver, CIAN)
            print_color("\nSi quieres añadir un nuevo objetivo a un hábito existente, introduce el nombre del hábito.",CIAN)

            nombre = pedir_nombre_registro()
            
            # da la opción de introducir volver y salir en todas sus variables
            if normalizar(nombre) in ("volver","salir",""):
                return False
            
            categorias = mostrar_csv_diccionario("categorias")
            cat_dict = {cat["categoria"]: cat["emoticono"] for cat in categorias}
            
            
            categorias_lista = sorted(cat_dict.keys())
            if categorias_lista:
                # si no está registrado, prosigue con el resto de inputs
                print("\nCategorías disponibles:")
                
                for i, cat in enumerate(categorias_lista, 1):
                    print(f"{i}. {cat} {cat_dict[cat]}")

                categoria = input("\nIntroduce una categoria de la lista o añade una nueva: ")
            else:
                categoria = input("Categoría: ")
           
            if categoria in cat_dict:
                emoticono = cat_dict[categoria]
            else:
                emoticono = input("Introduce un emoticono asociado: ")

            while True:
                lista_tipos = ["diario","semanal","mensual","anual"]
                tipo = input(f"Objetivo ({lista_tipos}): ")
                if normalizar(tipo) not in lista_tipos:
                    continue
                break
                    
            while True:
                objetivo = input("Objetivo (horas): ")
                
                # comprueba que las horas sean mayores que 0 y no contengan letras u otros caracteres
                
                if validar_horas(objetivo):
                    objetivo = validar_horas(objetivo)
                    registrar_categoria(categoria, emoticono)
                    id_categoria = dev_categoria_id(categoria)
                    id_habito = registrar(nombre, id_categoria)
                    registrar_objetivo(id_habito, tipo, objetivo)
                    print_color("\nSe ha añadido el hábito "+nombre+" en la categoría "+categoria+" con un objetivo "+tipo+" de "+objetivo+" horas.",VERDE)

                    otro_objetivo(id_habito, tipo, lista_tipos, nombre, categoria)
                else:
                    continue
                break

            seguir = input("\n¿Quieres introducir un nuevo hábito? s/n: ")
            lista = mostrar_registros()
            if preguntar_seguir(seguir):
                if not lista:
                    break
                continue
            else:
                break

def opcion_temporizador():
    lista = mostrar_temporizadores()
    while True: #empieza el bucle para seguir creando temporizadores
  
            lista = mostrar_registros() # devuelve el listado de habitos registrados
            lista_minus = [item.lower() for item in lista]
            print_color("\nAñadir un nuevo temporizador",INVERSION)
            print("\nHábitos registrados: \n")

            # recorre el listado, numerandolo con el nombre al lado
            for i, item in enumerate(sorted(lista), start=1):
                print(f"- {item}")
            print_color(volver, CIAN)
            
            nombre = pedir_nombre_temp(lista_minus,lista)
            if nombre == None:
                return False
            while True:
                fecha = pedir_fecha_temp()  
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
                        print_color(f"\nSe ha registrado {horas} en el temporizador {nombre} con fecha {fecha}",VERDE)
                        break # una vez es correcto, sale del bucle de horas y dias y vuelve al bucle original
                break
            seguir = input("\n¿Quieres introducir un nuevo temporizador? s/n: ")
            if preguntar_seguir(normalizar(seguir)):
                continue
            else:
                break    

def opcion_borrar():
    # muestra previamente todos los registros a eliminar
    lista = mostrar_registros()
    if lista:
        while True:
            lista = mostrar_registros()
            print("\nEstos son los hábitos ya registrados: \n")
            for i, item in enumerate(lista, start=1):
                print(f"{i} - {item}")
            print_color(volver, CIAN)
            print_color("\nEliminar un hábito\n",INVERSION)
            borrar = pedir_habito_borrar()
            if borrar == None:
                break
            lista = mostrar_registros()
            if lista:
                seguir = input("\n¿Quieres eliminar otro hábito? s/n: ")
                if preguntar_seguir(normalizar(seguir)):
                    continue
                else:
                    break    
            else:
                break

    else:
        print_color("\nNo existe ningún hábito a eliminar.",CIAN)

def opcion_borrar_tempo():
    # muestra previamente todos los registros a eliminar
    lista = mostrar_temporizadores()

    if lista:
        while True:
            #dev_habito_id
            #obtener_nombre_idhabito = id_habito_nombre()
            print("\nEstos son los temporizadores ya registrados: \n")
            for i, item in enumerate(lista, start=1):
                    nombre = dev_nombre_habito_id(item["id_habito"])
                    print(f"{i} - {item["fecha"]}, {item["horas"]} horas ({nombre}) ")
            print_color(volver,CIAN)
            print_color("\nEliminar un temporizador\n",INVERSION)
            borrar = pedir_temporizador_borrar()
            
            if borrar == None:
                return False
            else:
                seguro = input(f"\n{ROJO}¿Estás seguro de que quieres borrar el temporizador {dev_nombre_habito_id(borrar["id_habito"])} con {borrar["horas"]} horas registradas del día {borrar["fecha"]}?\nEsta acción ELIMINARÁ el temporizador de forma PERMANENTE. 4s/n: {RESET}")
                seguro = seguro.lower()

                if seguro == "s" or seguro == "si":
                    habito = borrar_temporizador(borrar["id"],borrar)
                    print_color(f"\nTemporizador eliminado con éxito.",VERDE)
                elif seguro == "n" or seguro == "no":
                    continue
            lista = mostrar_temporizadores()
            if lista:
                seguir = input("\n¿Quieres eliminar otro temporizador? s/n: ")
                if preguntar_seguir(normalizar(seguir)):
                    continue
                else:
                    break    
            else:
                break

    else:
        print_color("\nNo existe ningún temporizador a eliminar.",CIAN)

def opcion_borrar_categoria():
    # muestra previamente todos los registros a eliminar
    lista = mostrar_categorias()

    if lista:
        while True:

            print("\nEstos son las categorias ya registradas: \n")
            for i, item in enumerate(lista, start=1):
                print(f"{i} - {item}")
            print_color(volver,CIAN)
            print_color("\nEliminar una categoría\n",INVERSION)
            borrar = pedir_categoria_borrar()
            if borrar == None:
                return False
            lista = mostrar_categorias()
            if lista:
                seguir = input("\n¿Quieres eliminar otra categoría? s/n: ")
                if preguntar_seguir(normalizar(seguir)):
                    continue
                else:
                    break    
            else:
                break
    else:
        print_color("\nNo existe ninguna categoria a eliminar.",CIAN)

def opcion_borrar_todo():
    lista1 = mostrar_temporizadores()
    lista2 = mostrar_registros()
    lista3 = mostrar_categorias()
    lista4 = mostrar_csv("objetivos")

    if lista1 or lista2 or lista3 or lista4:
        seguro = input(f"\n{ROJO}¿Estás seguro de que quieres borrar todos los registros? s/n:{RESET} ")

        seguro = seguro.lower()

        if seguro == "s" or seguro == "si":

            borrar_csv("categorias.csv")
            borrar_csv("habitos.csv")
            borrar_csv("temporizadores.csv")
            borrar_csv("objetivos.csv")
            print(f"{VERDE}Todos los registros han sido eliminados.{RESET}")
        elif seguro == "n" or seguro == "no":
            limpiar_pantalla()
            return
    else:
        print_color("No existen elementos a eliminar.",CIAN)

def opcion_modi_habito():
    # muestra previamente todos los registros a eliminar
    lista = mostrar_registros()

    if lista:
        while True:
            lista_todo = mostrar_csv("habitos")
            #ordena la lista por nombre (el segundo campo del csv)
            lista_todo = sorted(lista_todo, key=lambda x: x[1])

            print("\nEstos son los hábitos ya registrados: \n")
            for i, item in enumerate(lista_todo, start=1):
                habito = item[1]
                tipo_objetivo = item[3]
                objetivo_horas = item[4]
                print(f"{i} - {habito} (Objetivo {tipo_objetivo} de {objetivo_horas} horas)")
            print_color(volver, CIAN)
            print_color("\nModificar un hábito\n",INVERSION)
            modificar = pedir_habito_modi()
           
            if modificar == "":
                break
            lista = mostrar_registros()
            if lista:
                seguir = input("\n¿Quieres modificar otro hábito? s/n: ")
                if preguntar_seguir(normalizar(seguir)):
                    continue
                else:
                    break    
            else:
                break
    else:
        print_color("\nNo existe ningún hábito a modificar.",CIAN)

def opcion_modi_tempo():
    # muestra previamente todos los registros a eliminar
    lista = mostrar_registros()

    if lista:
        while True:
            lista_todo = mostrar_csv("temporizadores")
            #ordena la lista por fecha (el tercer campo del csv)
            lista_todo = sorted(lista_todo, key=lambda x: x[3])

            print("\nEstos son los temporizadores ya registrados: \n")
            for i, item in enumerate(lista_todo, start=1):
                temporizador = dev_nombre_habito_id(item[1])
                tiempo = item[2]
                fecha = item[3]
                print(f"{i} - {fecha} - {tiempo} horas ({temporizador})")

            print_color(volver, CIAN)
            print_color("\nModificar un temporizador\n",INVERSION)
            modificar = pedir_tempo_modi(lista_todo)
           
            if modificar == "":
                break
            lista = mostrar_registros()
            if lista:
                seguir = input("\n¿Quieres modificar otro hábito? s/n: ")
                if preguntar_seguir(normalizar(seguir)):
                    continue
                else:
                    break    
            else:
                break
    else:
        print_color("\nNo existe ningún hábito a modificar.",CIAN)

def opcion_modi_categoria():
    lista = mostrar_categorias()

    if lista:
        while True:
            lista_todo = mostrar_csv("categorias")


            lista_todo = sorted(lista_todo, key=lambda x: x[1])
            print("\nEstos son las categorias ya registradas: \n")

            for i, item in enumerate(lista_todo, start=1):
                id_categoria = item[0]
                categoria = item[1]
                emoticono = item[2]
                print(f"{i} - {categoria} {emoticono}")

            print_color(volver, CIAN)
            print_color("\n Modificar una categoria\n",INVERSION)

            modificar = pedir_categoria_modi(lista_todo)

            if modificar == "volver":
                break
            lista = mostrar_registros()
            
            if lista:
                seguir = input("\n¿Quieres modificar otro hábito? s/n: ")
                if preguntar_seguir(normalizar(seguir)):
                    continue
                else:
                    break    
            else:
                break

def opcion_estadistica_objetivo():
    diarios, semanales, mensuales, anuales, habitos, temporizadores, categorias = agrupar_datos_csv()

    lineas = [
        print_color_pausa("===== Objetivos registrados ======",CIAN),
        
        *generar_bloque_objetivo("días", diarios, temporizadores, "dia", "Día", 7),
        *generar_bloque_objetivo("semanas", semanales, temporizadores, "semana", "Semana", 4),
    ]
    
    imprimir_con_pausa(lineas)

    while True:
        mostrar_mas = normalizar(input(
            "\nPulsa 'M' para ver los objetivos mensuales, 'A' para los anuales o 'ENTER' para salir: "
        ))

        if mostrar_mas in ("","volver","salir"):
            break
        if mostrar_mas == "m":
            lineas_mes = generar_bloque_objetivo("meses", mensuales, temporizadores, "mes", "Mes", 4)
            imprimir_con_pausa(lineas_mes)
        elif mostrar_mas == "a":
            lineas_año = generar_bloque_objetivo("años", anuales, temporizadores, "año", "Año", 4)
            imprimir_con_pausa(lineas_año)


def opcion_estadistica_resumen():
    salir = False
    while not salir:

        diarios, semanales, mensuales, anuales, habitos, temporizadores, categorias = agrupar_datos_csv()


        lineas = [
        print_color_pausa("\n=======================================",CIAN),
        print_color_pausa("  📊 RESUMEN DE HÁBITOS REGISTRADOS    ",CIAN),
        print_color_pausa("=======================================",CIAN),
        
        *generar_bloque_resumen("DIARIOS", diarios, temporizadores, "dia", categorias),
        *generar_bloque_resumen("SEMANALES", semanales, temporizadores, "semana", categorias),
    ]
        imprimir_con_pausa(lineas)

        while True:
            mostrar_mas = normalizar(input(
                "\nPulsa 'M' para ver los objetivos mensuales, 'A' para los anuales o 'ENTER' para salir: "
            ))

            if mostrar_mas in ("","volver","salir"):
                salir = True  # Indicamos que queremos salir de todo
                break  # Salimos del bucle interno
            if mostrar_mas == "m":
                lineas_mes = generar_bloque_resumen("MENSUALES", mensuales, temporizadores, "mes",categorias)
                imprimir_con_pausa(lineas_mes)
            elif mostrar_mas == "a":
                lineas_año = generar_bloque_resumen("ANUALES", anuales, temporizadores, "año",categorias)
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

        mostrar_mas = normalizar(input(
            "\nPulsa 'ENTER' para salir: "
        ))

        if mostrar_mas in ("","volver","salir"):
            mostrar_mas = True
