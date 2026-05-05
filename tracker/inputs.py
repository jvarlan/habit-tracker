from datetime import datetime
import time
import threading
from .checks import normalizar, validar_horas, comprobar_horas_temp_24, comprobar_registro, validar_borrar_temporizador, comprobar_categoria
from .mostrar import mostrar_registros, mostrar_temporizadores, mostrar_categorias, mostrar_csv, mostrar_csv_diccionario, mostrar_objetivos
from .guardar import registrar_objetivo, registrar_categoria
from .contar import contar_csv_n, contar_csv_id
from .devolver import dev_habito_id, dev_habito_datos, dev_nombre_habito_id, dev_tipo_objetivo, dev_idhabito_temporizador, dev_lista_objetivos_cat, dev_categoria_id, dev_nombre_categoria_id, dev_lista_habitos_cat, dev_lista_temporizadores_cat
from .borrar import borrar_temporizadores, borrar_habito, borrar_categoria, borrar_objetivos_id_habito
from .modificar import modificar_habito, modificar_temporizador, modificar_categoria
from .utilidades import ROJO, VERDE, CIAN, INVERSION, RESET,print_color, cronometro, esperar_enter, horas_a_segundos, preguntar_seguir, limpiar_pantalla

def pedir_nombre_registro(volver):
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
  
        nombre = input("\nNombre a registrar: ")
     # devuelve el número de veces que el nombre está registrado
        comprobado = comprobar_registro(nombre)

        # si está registrado, vuelve a pedir el nombre
        if comprobado == 0:
            return nombre
        elif comprobado > 0:
            # aqui no deberia ahora obligar a repetir el nombre, ya que ahora se añadirán nuevos objetivos al introducir uno ya existente.

            datos_habito = dev_habito_datos(nombre)
            id_habito = datos_habito['id']
            categoria = dev_nombre_categoria_id(datos_habito['id_categoria'])
            lista_tipos_usados = dev_tipo_objetivo(id_habito)
            lista_tipos = ['diario','semanal','mensual','anual']

            resultado = otro_objetivo(id_habito, lista_tipos_usados, lista_tipos, nombre, categoria)
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
    while True:
        nombre = input("Nombre a temporizar: ")
        nombre = normalizar(nombre)

        for i, item in enumerate(lista_minus):
            if item == nombre:
                return lista[i]
        if normalizar(nombre) in ("volver","salir",""):
            return None
        else:
            print_color(f"Introduce un temporizador de la lista.",ROJO)

def pedir_horas_temp():
    while True:
        registro = input("Pulsa 'M' para registro manual o 'A' para automático: ")
        if normalizar(registro) == "m":
            horas = input("Duración de la actividad (HH:MM:SS): ")
            if validar_horas(horas):
                horas = validar_horas(horas)
                return horas

        elif normalizar(registro) == "a":
            stop_event = threading.Event()
            resultado = []

            print_color("Pulsa ENTER cuando quieras parar el cronómetro... ",CIAN)
            
            
            hilo_input = threading.Thread(target=esperar_enter, args=(stop_event,))
            hilo_input.start()

            hilo_crono = threading.Thread(target=cronometro, args=(stop_event, resultado))
            hilo_crono.start()

            hilo_crono.join()
            hilo_input.join()

            horas = resultado[0]
            if validar_horas(horas):
                return horas
        return False
def pedir_fecha_temp():
    while True:
            fecha = input("Introduce la fecha (AAAA-MM-DD) o déjalo vacío para hoy: ")
            
            if fecha == "":
                fecha = datetime.now().date()
            else:
                try:
                    fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
                    fecha_hoy = datetime.now().date()

                    if fecha > fecha_hoy:
                        print_color(f"La fecha no puede ser superior a la fecha actual.",ROJO)
                        continue
                except ValueError:
                    print_color(f"Formato incorrecto. Debe ser AAAA-MM-DD",ROJO)
                    continue
            return fecha
def pedir_habito_borrar():
    while True:
        lista = mostrar_registros()
        if lista:
            borrar = input("Introduce el nombre del elemento a borrar: ")
            if normalizar(borrar) in ("volver","salir",""):
                return None
            
            borrar_id = dev_habito_id(borrar)
            temporizadores = contar_csv_n("temporizadores",borrar_id,0)
            objetivos = contar_csv_id("objetivos",borrar_id,1)
            habitos = contar_csv_n("habitos",borrar_id,0)

            if habitos == False:
                print_color("Este hábito no existe.",ROJO)
                continue
            else:
                seguro = input(f"\n{ROJO}El hábito {borrar} tiene {objetivos} objetivos y {temporizadores} registros de horas asociados. Esta acción borrará los DATOS de forma PERMANENTE. ¿Quieres continuar? s/n: {RESET}")
                seguro = seguro.lower()
                
                if seguro == "s" or seguro == "si":
                    registros = borrar_temporizadores(borrar_id,temporizadores)
                    habito = borrar_habito(borrar,borrar_id)
                    borrar_objetivos_id_habito(borrar_id)
                    print_color(f"\nEl hábito {borrar} se ha eliminado con éxito.",VERDE)
                    return True
                elif seguro == "n" or seguro == "no":
                    return
        else:
            return None
def pedir_categoria_borrar():
    while True:
        lista = mostrar_categorias()
        if lista:
            borrar = input("Introduce el nombre del elemento a borrar: ")
            if normalizar(borrar) in ("volver","salir",""):
                return None
            if comprobar_categoria(normalizar(borrar)) is True:
        
                id_categoria = dev_categoria_id(borrar)
                lista_habitos = dev_lista_habitos_cat(id_categoria)
                lista_objetivos_categoria = dev_lista_objetivos_cat(lista_habitos)
                lista_temporizadores = dev_lista_temporizadores_cat(lista_habitos)

                seguro = input(f"{ROJO}\nLa categoria {borrar} tiene {len(lista_objetivos_categoria)} objetivos, {len(lista_habitos)} hábitos, y {len(lista_temporizadores)} registros de tiempo asociados. Esta acción eliminará los DATOS de forma PERMANENTE.\n¿Quieres continuar? s/n: {RESET}")
                seguro = seguro.lower()
                
                if seguro == "s" or seguro == "si":
                    habito = borrar_categoria(borrar,id_categoria,lista_habitos,lista_temporizadores, lista_objetivos_categoria)
                    print_color(f"\nLa categoria {borrar} y todos sus elementos relacionados han sido borrados con éxito.",VERDE)
                    return False
                elif seguro == "n" or seguro == "no":
                    return
            else:
                print_color("Opción no válida.",ROJO)
                continue
        else:
            return None

def pedir_objetivo_borrar():
    while True:
        lista = mostrar_objetivos()
        if lista:
        
            borrar = input("Introduce el número del elemento a borrar: ")
            if normalizar(borrar) in ("volver","salir",""):
                return None
            else:
                validado = validar_borrar_temporizador(borrar,lista)
                if validado is None:
                    continue
                else:
                    return validado
        else:
            return None


def pedir_temporizador_borrar():
    while True:
        lista = mostrar_temporizadores()
        if lista:
        
            borrar = input("Introduce el número del elemento a borrar: ")
            if normalizar(borrar) in ("volver","salir",""):
                return None
            else:
                validado = validar_borrar_temporizador(borrar,lista)
                if validado is None:
                    continue
                else:
                    return validado
        else:
            return None
        
def pedir_habito_modi():
    while True:
        lista = mostrar_registros()
        if lista:
            habito_modificar = input("Introduce el nombre del elemento a modificar: ")
        if normalizar(habito_modificar) in ("volver","salir",""):
                return ""
              
        habitos = contar_csv_id("habitos",dev_habito_id(habito_modificar),0)

        if habitos == False:
            print_color("Este hábito no existe.",ROJO)
            continue
        else:
            todo_habito = mostrar_csv_diccionario("habitos")
            for fila in todo_habito:
                if fila["habito"].lower() == habito_modificar.lower():
                    habito = fila["habito"]
                    categoria = dev_nombre_categoria_id(fila["id_categoria"])
            print_color(f"Hábito actual: {habito}",CIAN)
            contador = 0

            seguro = input(f"{ROJO}¿Quieres modificar el nombre del hábito {habito}? s/n: {RESET}")
            seguro = seguro.lower()
            
            if seguro in ("s","si"):
                while True:
                    habito = input(f"Nuevo nombre: ")
                    contador +=1
                        # devuelve el número de veces que el nombre está registrado
                    comprobado = comprobar_registro(habito)

                    # si está registrado, vuelve a pedir el nombre
                    if comprobado > 0:
                        print_color("Esté hábito ya está registrado. Por favor, introduce uno nuevo.", ROJO)
                        continue
                    else: 
                        break
            seguro = input(f"{ROJO}¿Quieres modificar la categoría? s/n: {RESET}")
            seguro = seguro.lower()
            
            if seguro in ("s","si"):
                while True:
                    lista_todo = mostrar_csv_diccionario("categorias")
                    modificar_categoria = input("Nueva categoría: ")
                    if any(item.get("categoria") == modificar_categoria for item in lista_todo):
                        id_categoria = dev_categoria_id(modificar_categoria)
                        contador +=1
                        break
                    else:
                        print_color("Has añadido una nueva categoría.",CIAN)
                        emoticono = input(f"Introduce un emoticono para la nueva categoría {modificar_categoria}: ")
                        registrar_categoria(modificar_categoria, emoticono)
                        id_categoria = dev_categoria_id(modificar_categoria)
                        contador +=1
                        break
            else:
                modificar_categoria = categoria
                   
            if contador > 0:
                modificar_habito(habito,dev_habito_id(habito_modificar),id_categoria)
                print_color(f"\nEl hábito {habito} ha sido cambiado con éxito por {habito_modificar}. La categoría {categoria} ha sido cambiada por {modificar_categoria}",VERDE)
                return
            else:
                print_color("No se ha modificado nada.",CIAN)
                break

def pedir_tempo_modi(lista_todo):
    while True:

        if lista_todo:
            try:
                modificar = input("Introduce el número del temporizador a modificar: ")
                
                if normalizar(modificar) in ("volver","salir"):
                    return ""
                modificar = int(modificar) 

                id_temporizador = lista_todo[modificar-1][0]
                
                temporizadores = contar_csv_id("temporizadores",id_temporizador,0)           
            except ValueError:
                print_color(f"Formato incorrecto. Debes introducir un número de la lista.",ROJO)
                continue
            except IndexError:
                print_color("Este temporizador no existe.",ROJO)
                continue

            todo_habito = mostrar_csv("temporizadores")
            for fila in todo_habito:
                if fila[0] == id_temporizador:
                    habito = dev_nombre_habito_id(fila[1])
                    horas = fila[2]
                    fecha = fila[3]
            print_color(f"Hábito actual: {habito}",CIAN)
            print_color(f"Hora actual: {horas}",CIAN)
            print_color(f"Fecha actual: {fecha} ",CIAN)

            contador = 0

            seguro = input(f"{ROJO}¿Quieres modificar las horas? s/n: {RESET}")
            seguro = seguro.lower()
            
            if seguro in ("s","si"):
                while True:
                    nueva_hora = pedir_horas_temp()
                    id_habito = lista_todo[modificar-1][1]
                    
                    contador_horas_24 = comprobar_horas_temp_24(datetime.strptime(fecha, "%Y-%m-%d").date(), id_habito)
                    contador_horas_24_total = int(contador_horas_24) - int(horas_a_segundos(horas)) + int(horas_a_segundos(nueva_hora))
                    
                    if contador_horas_24_total > 24 * 3600:
                        print_color(f"Este temporizador ya tiene 24 horas registradas en este día.",ROJO)
                        continue
                    else:
                        contador +=1
                        break
            else:
                nueva_hora = horas

            seguro = input(f"{ROJO}¿Quieres modificar la fecha del registro? s/n: {RESET}")
            seguro = seguro.lower()
            
            if seguro in ("s","si"):
                nueva_fecha = pedir_fecha_temp()
                contador +=1
            else:
                nueva_fecha = fecha

            if contador > 0:
                
                modificar_temporizador(id_temporizador,nueva_hora,nueva_fecha)
                id_habito = dev_idhabito_temporizador(id_temporizador)
                print_color(f"\nEl temporizador {dev_nombre_habito_id(id_habito)} con {horas} horas registradas el día {fecha} ha sido cambiado con éxito por {nueva_hora} horas con fecha {nueva_fecha}.",VERDE)
                return
            else:
                print_color("No se ha modificado nada.",CIAN)
                return
            
def pedir_categoria_modi(lista_todo):
    while True:
        if lista_todo:
                modificar = input("Introduce el nombre de la categoría a modificar: ")
                for item in lista_todo:
                    if item["categoria"] == modificar:
                        emoticono = item["emoticono"]
                        break
                if normalizar(modificar) in ("volver","salir",""):
                    return "volver"
                if any(item.get("categoria") == modificar for item in lista_todo):

                    for lista in lista_todo:
                        if modificar == lista["categoria"]:
                            id_categoria = lista["id"]
                else:
                    print_color("Has añadido una nueva categoría.",CIAN)
                    emoticono = input(f"Introduce un emoticono para la categoría {modificar}: ")
                    registrar_categoria(modificar, emoticono)


                categorias = contar_csv_id("categorias",id_categoria,0)
                # contador para contabilizar si el usuario modifica algo o no
                contador = 0
                seguro = input(f"{ROJO}¿Quieres modificar el nombre de la categoria? s/n: {RESET}")
                seguro = seguro.lower()
                
                if seguro in ("s","si"):
                    nueva_categoria = input("Introduce el nuevo nombre para la categoria: ")
                    contador +=1
                else:
                    nueva_categoria = modificar
                seguro = input(f"{ROJO}¿Quieres modificar el emoticono asociado? s/n: {RESET}")
                seguro = seguro.lower()

                if seguro in ("s","si"):
                    nuevo_emoticono = input("Introduce el nuevo emoticono: ")
                    contador +=1
                else:
                    nuevo_emoticono = emoticono
 
            
                if categorias:
                    if contador > 0:
                        modificar_categoria(id_categoria,nueva_categoria, nuevo_emoticono)

                        print_color("Categoria cambiada con éxito.",VERDE)

                        return
                    else:
                        print_color("No se ha modificado nada.",ROJO)
                        return
                
def otro_objetivo(id_habito, tipo, lista_tipos, nombre, categoria):
        
        while True:
            
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
            
            tipos_restantes = []

            for ltipos in lista_tipos:
                if isinstance(ltipos, str):
                    limpio = ltipos.strip().lower()
                    if limpio and limpio not in tipos_usados:
                        tipos_restantes.append(ltipos)

            if not tipos_restantes:
                print_color("\nNo quedan más tipos disponibles para este hábito.",ROJO)
                return True

            otro_habito = input("\n¿Quieres añadir un objetivo diferente para este hábito? s/n: ")

            if not preguntar_seguir(normalizar(otro_habito)):
                break
            
            while True:
                tipo_ad = normalizar(input(f"Otro tipo ({tipos_restantes}): "))
                if normalizar(tipo_ad) in ("","volver","salir"):
                    limpiar_pantalla()
                    return
                if tipo_ad not in tipos_restantes:
                    continue
                break

            while True:
                objetivo_ad = input("Otro objetivo (horas): ")
                if validar_horas(objetivo_ad):
                    objetivo_ad = validar_horas(objetivo_ad)
                    registrar_objetivo(id_habito, tipo_ad, objetivo_ad)
                    print_color("\nSe ha añadido el hábito "+nombre+" en la categoría "+categoria+" con un objetivo "+tipo_ad+" de "+objetivo_ad+" horas.",VERDE)
                    break
                break
        
