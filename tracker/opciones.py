from .utilidades import ROJO, VERDE, CIAN, INVERSION, RESET, print_color, preguntar_seguir
from .checks import comprobar_horas_temp,comprobar_horas_temp_24, normalizar, validar_horas
from .guardar import registrar, registrar_categoria, habito
from .mostrar import mostrar_registros, mostrar_registros_todo, mostrar_temporizadores, mostrar_temporizadores_todo, mostrar_categorias
from .devolver import dev_categoria_id, dev_habito_id
from .inputs import pedir_nombre_temp, pedir_horas_temp, pedir_fecha_temp, pedir_nombre_registro, pedir_categoria_borrar, pedir_temporizador_borrar, pedir_habito_borrar, pedir_habito_modi, pedir_tempo_modi
from .borrar import borrar_csv, borrar_temporizador

volver = f"\nEscribe 'volver' si quieres salir al menú de opciones."
volver2 = f"\n............................................................................"


def opcion_registro():

        while True:
            lista = mostrar_registros()
            print_color("\nRegistrar un nuevo hábito",INVERSION)
            if lista:
                print("\nHábitos registrados: \n")
                # recorre el listado, numerandolo con el nombre al lado
                for i, item in enumerate(sorted(lista), start=1):
                    print(f"{i}. {item}")
            print_color(volver, CIAN)

            nombre = pedir_nombre_registro()
            
            # da la opción de introducir volver y salir en todas sus variables
            if normalizar(nombre) == "volver" or normalizar(nombre) == "salir":
                return False
                
            # si no está registrado, prosigue con el resto de inputs
            categoria = input("Categoria: ")

            while True:
                objetivo = input("Objetivo (horas): ")
                
                # comprueba que las horas sean mayores que 0 y no contengan letras u otros caracteres
                
                if validar_horas(objetivo):
                    registrar_categoria(categoria)
                    id_categoria = dev_categoria_id(categoria)
                    registrar(nombre, id_categoria, objetivo)
                    print_color("\nSe ha añadido el hábito "+nombre+" en la categoría "+categoria+" con un objetivo de "+objetivo+" horas.",VERDE)
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
            print_color("Añadir un nuevo temporizador",INVERSION)
            print("\nHábitos registrados: \n")

            # recorre el listado, numerandolo con el nombre al lado
            for i, item in enumerate(sorted(lista), start=1):
                print(f"{i}. {item}")
            print_color(volver, CIAN)
            
            nombre = pedir_nombre_temp(lista_minus,lista)
            if normalizar(nombre) == "volver" or normalizar(nombre) == "salir":
                return False
            while True:
                fecha = pedir_fecha_temp()  
                temporizadores = mostrar_temporizadores()
                contador_horas_24 = comprobar_horas_temp_24(temporizadores, fecha, nombre)
                if contador_horas_24 >= 24:
                    print_color(f"Este temporizador ya tiene 24 horas registradas en este día.",ROJO)
                    break
                while True:
                    horas = pedir_horas_temp()
                    id_habito = dev_habito_id(nombre)
                    
                    contador_horas = comprobar_horas_temp(temporizadores,horas,fecha,nombre)

                    if contador_horas > 24:
                        print_color("El total de horas registradas para esta actividad no puede ser mayor de 24",ROJO)
                        continue #si la actividad supera las 24 horas el mismo día, vuelve a pedir las horas
                    else:     
                        habito(id_habito,nombre,horas,fecha)
                        print_color(f"\nSe han añadido {horas} horas al temporizador {nombre} con fecha {fecha}",VERDE)
                        break # una vez es correcto, sale del bucle de horas y dias y vuelve al bucle original
                break
            seguir = input("\n¿Quieres introducir un nuevo hábito? s/n: ")
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
                seguir = input("\n¿Quieres eliminar otro temporizador? s/n: ")
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
            lista = mostrar_temporizadores()
            print("\nEstos son los temporizadores ya registrados: \n")
            for i, item in enumerate(lista, start=1):
                print(f"{i} - {item["nombre"]}: Horas '{item["horas"]}' Fecha '{item["fecha"]}'")
            print_color(volver,CIAN)
            print_color("\nEliminar un temporizador\n",INVERSION)
            borrar = pedir_temporizador_borrar()
            if borrar == None:
                return False
            else:
                seguro = input(f"\n{ROJO}¿Estás seguro de que quieres borrar el hábito {borrar["nombre"]} con {borrar["horas"]} horas registradas del día {borrar["fecha"]}? s/n: {RESET}")
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

    if lista1 or lista2 or lista3:
        seguro = input(f"\n{ROJO}¿Estás seguro de que quieres borrar todos los registros? s/n:{RESET} ")

        seguro = seguro.lower()

        if seguro == "s" or seguro == "si":

            borrar_csv("categorias.csv")
            borrar_csv("habitos.csv")
            borrar_csv("temporizadores.csv")
            print(f"{VERDE}Todos los registros han sido eliminados.{RESET}")
        elif seguro == "n" or seguro == "no":
            return
    else:
        print_color("No existen elementos a eliminar.",CIAN)

def opcion_modi_habito():
    # muestra previamente todos los registros a eliminar
    lista = mostrar_registros()

    if lista:
        while True:
            lista_todo = mostrar_registros_todo()
            #ordena la lista por nombre (el segundo campo del csv)
            lista_todo = sorted(lista_todo, key=lambda x: x[1])

            print("\nEstos son los hábitos ya registrados: \n")
            for i, item in enumerate(lista_todo, start=1):
                habito = item[1]
                objetivo = item[3]
                print(f"{i} - {habito} ({objetivo} horas)")
            print_color(volver, CIAN)
            print_color("\nModificar un hábito\n",INVERSION)
            modificar = pedir_habito_modi()
           
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
    else:
        print_color("\nNo existe ningún hábito a modificar.",CIAN)

def opcion_modi_tempo():
    # muestra previamente todos los registros a eliminar
    lista = mostrar_registros()

    if lista:
        while True:
            lista_todo = mostrar_temporizadores_todo()
            #ordena la lista por fecha (el cuarto campo del csv)
            lista_todo = sorted(lista_todo, key=lambda x: x[4])

            print("\nEstos son los temporizadores ya registrados: \n")
            for i, item in enumerate(lista_todo, start=1):
                temporizador = item[2]
                tiempo = item[3]
                fecha = item[4]
                print(f"{i} - {fecha} - {tiempo} horas ({temporizador})")

            print_color(volver, CIAN)
            print_color("\nModificar un temporizador\n",INVERSION)
            modificar = pedir_tempo_modi()
           
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
    else:
        print_color("\nNo existe ningún hábito a modificar.",CIAN)