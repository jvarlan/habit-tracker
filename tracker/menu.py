from .mostrar import mostrar_registros, mostrar_categorias, mostrar_temporizadores
from .opciones import opcion_registro, opcion_temporizador, opcion_borrar, opcion_borrar_todo, opcion_borrar_tempo, opcion_borrar_categoria, opcion_modi_habito, opcion_modi_tempo
from .utilidades import limpiar_pantalla
from .checks import normalizar
from .utilidades import ROJO, VERDE, CIAN, print_color

import tkinter as tk

# se guarda en una variable para luego simplemente mostrarlo en pantalla
volver = f"\nEscribe 'volver' si quieres salir del programa."
volver2 = f"\n..............................................."

#menu principal
def mostrar_menu():
    # se repite en bucle hasta que se pulse Salir
    while True:
        limpiar_pantalla()
        habitos = mostrar_registros()
        temporizadores = mostrar_temporizadores()
        categorias = mostrar_categorias()

        print_color("\n======== MENÚ HABIT TRACKER ========",VERDE)
        print("1. Registrar un nuevo hábito (100%)")
        if not habitos:
            print_color("2. Crear un temporizador (100%)",ROJO)
        else:
            print("2. Crear un temporizador (100%)")
        if not habitos and not temporizadores and not categorias:
            print_color("3. Eliminar elementos (100%)",ROJO)
        else:
            print("3. Eliminar elementos (100%)")
        print("4. Modificar elementos (En desarrollo)")
        print("5. Mostrar estadísticas (Por desarrollar)")
        print("6. Salir")
        print_color("====================================",VERDE)
        print_color(volver,CIAN)

        opcion = input("\nSelecciona una opción: ")

        if not seleccionar(opcion):
            break
#opciones del menú principal  
def opcion_1():
    limpiar_pantalla()
    opcion_registro()
    return True

def opcion_2():
    limpiar_pantalla()
    lista = mostrar_registros()
    if not lista:
        return True
    else:
        opcion_temporizador()
        return True

def opcion_3():
    limpiar_pantalla()
    lista = mostrar_categorias()
    if lista:
        mostrar_menu_borrar()
    else:
        print_color("\nActualmente no existe ningún elemento a eliminar.",CIAN)
    return True

def opcion_4():
    limpiar_pantalla()
    lista = mostrar_categorias()
    if lista:
        mostrar_menu_modificar()
    else:
        print_color("\nActualmente no existe ningún elemento a modificar.",CIAN)
    return True

def opcion_5():
    limpiar_pantalla()
    print("Prueba")
    print(mostrar_registros())
    return True

def opcion_6():
    print_color("Cerrando aplicación...",VERDE)
    return False
# según la elección escogida en el menú, redirige a las funciones de arriba
menu = {
    "1": opcion_1,
    "2": opcion_2,
    "3": opcion_3,
    "4": opcion_4,
    "5": opcion_5,
    "6": opcion_6
}

def seleccionar(opcion):
    # normaliza tanto volver como salir, y cierra el menú actual
    if normalizar(opcion) in ("volver", "salir"):
        return False
    # si la opción escogida está en el diccionario menu, redirige a la opción escogida
    if opcion in menu:
        return menu[opcion]()
    else:
        print_color("\nOpción no válida.",ROJO)
        return True

#menu borrar    
def mostrar_menu_borrar():
    while True:
        categorias = mostrar_categorias()
        if categorias:
            habitos = mostrar_registros()
            temporizadores = mostrar_temporizadores()
            categorias = mostrar_categorias()
        # se repite en bucle hasta que se pulse Salir
            print_color("\n========= MENÚ DE BORRADO =========",VERDE)
            if not habitos:
                print_color("1. Eliminar un hábito",ROJO)
            else:
                print("1. Eliminar un hábito")
            if not temporizadores:
                print_color("2. Eliminar un temporizador",ROJO)
            else:
                print("2. Eliminar un temporizador")

            print("3. Eliminar una categoría")
            print("4. Eliminar todos los elementos")
            print("5. Salir")
            print_color("====================================",VERDE)

            opcion = input("\nSelecciona una opción: ")
        else:
            break
        if not borrar(opcion):
            break

# las distintas opciones del menu borrar           
def borrar_1():
    opcion_borrar()
    limpiar_pantalla()
    return True
def borrar_2():
    opcion_borrar_tempo()
    limpiar_pantalla()
    return True
def borrar_3():
    opcion_borrar_categoria()
    limpiar_pantalla()
    return True
def borrar_4():
    opcion_borrar_todo()
    return True
def borrar_5():
    #sale del bucle
    return False

# diccionario que contiene la redirección de las funciones
menu_borrar = {
    "1": borrar_1,
    "2": borrar_2,
    "3": borrar_3,
    "4": borrar_4,
    "5": borrar_5
}
    
def borrar(opcion):
    # si el usuario escribe volver o salir también sale de la aplicación
    if normalizar(opcion) in("volver","salir"):
        return False
    # si la opcion coincide con una del diccionario menu_borrar, redirige a esa función
    if opcion in menu_borrar:
        return menu_borrar[opcion]()
    else:
        print_color("\nOpción no válida.\n",ROJO)
        return True

def mostrar_menu_modificar():
    while True:
        categorias = mostrar_categorias()
        if categorias:
            habitos = mostrar_registros()
            temporizadores = mostrar_temporizadores()
            categorias = mostrar_categorias()
        # se repite en bucle hasta que se pulse Salir
            print_color("\n========= MENÚ DE MODIFICACIÓN =========",VERDE)
            if not habitos:
                print_color("1. Modificar un hábito",ROJO)
            else:
                print("1. Modificar un hábito")
            if not temporizadores:
                print_color("2. Modificar un temporizador",ROJO)
            else:
                print("2. Modificar un temporizador")

            print("3. Modificar una categoría")
            print("4. Modificar todos los elementos")
            print("5. Salir")
            print_color("====================================",VERDE)

            opcion = input("\nSelecciona una opción: ")
        else:
            break
        if not modificar(opcion):
            break

# las distintas opciones del menu modificar           
def modi_1():
    opcion_modi_habito()
    limpiar_pantalla()
    return True
def modi_2():
    opcion_modi_tempo()
    limpiar_pantalla()
    return True
def modi_3():
    print("Now in development")
    return False
    #opcion_borrar_categoria()
    #limpiar_pantalla()
    #return True
def modi_4():
    print("Now in development")
    return False
    #opcion_borrar_todo()
    #return True
def modi_5():
    #sale del bucle
    return False
# diccionario que contiene la redirección de las funciones
menu_modificar = {
    "1": modi_1,
    "2": modi_2,
    "3": modi_3,
    "4": modi_4,
    "5": modi_5
}

def modificar(opcion):
    # si el usuario escribe volver o salir también sale de la aplicación
    if normalizar(opcion) in("volver","salir"):
        return False
    # si la opcion coincide con una del diccionario menu_borrar, redirige a esa función
    if opcion in menu_modificar:
        return menu_modificar[opcion]()
    else:
        print_color("\nOpción no válida.\n",ROJO)
        return True