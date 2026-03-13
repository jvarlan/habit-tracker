from datetime import datetime
from .checks import normalizar, validar_horas, comprobar_horas_temp_24, comprobar_registro, validar_borrar_temporizador, comprobar_categoria
from .mostrar import mostrar_registros, mostrar_temporizadores, mostrar_categorias, mostrar_csv
from .contar import contar_csv_n, contar_csv_id
from .devolver import dev_habito_id, dev_nombre_habito_id, dev_categoria_id, dev_lista_habitos_cat, dev_lista_temporizadores_cat
from .borrar import borrar_temporizadores, borrar_habito, borrar_categoria
from .modificar import modificar_habito, modificar_temporizador, modificar_categoria
from .utilidades import ROJO, VERDE, CIAN, RESET,print_color

def pedir_nombre_registro():
     while True:
        nombre = input("\nNombre a registrar: ")
     # devuelve el número de veces que el nombre está registrado
        comprobado = comprobar_registro(nombre)

        # si está registrado, vuelve a pedir el nombre
        if comprobado > 0:
            print_color("Esté hábito ya está registrado. Por favor, introduce uno nuevo.", ROJO)
            continue
        else: 
            return nombre        
def pedir_nombre_temp(lista_minus,lista):
    while True:
        nombre = input("Nombre a temporizar: ")
        nombre = normalizar(nombre)

        for i, item in enumerate(lista_minus):
            if item == nombre:
                return lista[i]
        if nombre in ("volver","salir"):
            return nombre
        else:
            print_color(f"Introduce un temporizador de la lista.",ROJO)

def pedir_horas_temp():
    while True:
        horas = input("Duración de la actividad (horas): ")
        if validar_horas(horas):
            return horas

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
            if normalizar(borrar) == "volver" or normalizar(borrar) == "salir":
                return None
            borrar = dev_habito_id(borrar)
            temporizadores = contar_csv_n("temporizadores",borrar)
            habitos = contar_csv_n("habitos",borrar)
            if habitos == False:
                print_color("Este hábito no existe.",ROJO)
                continue
            else:
                seguro = input(f"\n{ROJO}¿Estás seguro de que quieres borrar el hábito {borrar}?\nSe eliminarán {temporizadores} registros de horas asociados. s/n: {RESET}")
                seguro = seguro.lower()
                
                if seguro == "s" or seguro == "si":
                    registros = borrar_temporizadores(borrar,temporizadores)
                    habito = borrar_habito(dev_nombre_habito_id(borrar),borrar)
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
            if normalizar(borrar) == "volver" or normalizar(borrar) == "salir":
                return None
            if comprobar_categoria(normalizar(borrar)) is True:
        
                id_categoria = dev_categoria_id(borrar)
                lista_habitos = dev_lista_habitos_cat(id_categoria)
                lista_temporizadores = dev_lista_temporizadores_cat(lista_habitos,id_categoria)

                seguro = input(f"{ROJO}La categoria {borrar} tiene {len(lista_habitos)} hábitos asociados, con {len(lista_temporizadores)} registros de tiempo. ¿Estás seguro de que quieres borrar esta categoría? s/n: {RESET}")
                seguro = seguro.lower()
                
                if seguro == "s" or seguro == "si":
                    habito = borrar_categoria(borrar,id_categoria,lista_habitos,lista_temporizadores)
                    print_color(f"\nLa categoria {borrar} y todos sus elementos relacionados han sido borrados con éxito.",VERDE)
                    return False
                elif seguro == "n" or seguro == "no":
                    return
            else:
                print_color("Opción no válida.",ROJO)
                continue
        else:
            return None
        
def pedir_temporizador_borrar():
    while True:
        lista = mostrar_temporizadores()
        if lista:
        
            borrar = input("Introduce el número del elemento a borrar: ")
            if normalizar(borrar) == "volver" or normalizar(borrar) == "salir":
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
            modificar = input("Introduce el nombre del elemento a modificar: ")
        if normalizar(modificar) in ("volver","salir"):
                return "volver"
              
        habitos = contar_habitos(dev_habito_id(modificar))

        if habitos == False:
            print_color("Este hábito no existe.",ROJO)
            continue
        else:
            todo_habito = mostrar_csv("habitos")
            for fila in todo_habito:
                if fila[1].lower() == modificar.lower():
                    habito = fila[1]
                    objetivo = fila[3]
            print_color(f"Hábito actual: {habito}",CIAN)
            
            print_color(f"Objectivo actual: {objetivo} ",CIAN)
            contador = 0

            seguro = input(f"{ROJO}¿Quieres modificar el nombre? s/n: {RESET}")
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

            seguro = input(f"{ROJO}¿Quieres modificar el objetivo de horas? s/n: {RESET}")
            seguro = seguro.lower()
            
            if seguro in ("s","si"):
                while True:
                    objetivo = input(f"Nuevo objetivo: ")
                    if validar_horas(objetivo):
                        contador +=1
                        break
                    else:
                        continue

            if contador > 0:
                modificar_habito(habito,objetivo,dev_habito_id(modificar))
                print_color(f"\nEl hábito {modificar} ha sido cambiado con éxito por {habito} con un objetivo de {objetivo} horas.",VERDE)
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
                    return "volver"
                modificar = int(modificar) 

                id_temporizador = lista_todo[modificar-1][0]
                
                temporizadores = contar_csv_id("temporizadores",id_temporizador)           
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
                    contador_horas_24_total = int(contador_horas_24) - int(horas) + int(nueva_hora)
                    
                    if contador_horas_24_total > 24:
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
                
                print_color(f"\nEl temporizador {dev_nombre_habito_id(id_habito)} con {horas} horas registradas el día {fecha} ha sido cambiado con éxito por {nueva_hora} horas con fecha {nueva_fecha}.",VERDE)
                return
            else:
                print_color("No se ha modificado nada.",CIAN)
                return
            
def pedir_categoria_modi(lista_todo):
    while True:
        if lista_todo:
                modificar = input("Introduce el nombre de la categoría a modificar: ")

                if normalizar(modificar) in ("volver","salir"):
                    return "volver"
                for lista in lista_todo:
                    if modificar == lista[1]:
                        id_categoria = lista[0]

                categorias = contar_csv_id("categorias",id_categoria)

                nueva_categoria = input("Introduce el nuevo nombre para la categoria: ")
                if categorias:

                    modificar_categoria(id_categoria,nueva_categoria)

                    print_color("Categoria cambiada con éxito.",VERDE)

                    return
            