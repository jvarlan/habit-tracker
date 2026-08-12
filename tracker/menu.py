from .mostrar import mostrar_registros, mostrar_categorias, mostrar_temporizadores, mostrar_objetivos
from .opciones import opcion_registro, opcion_temporizador, opcion_borrar, opcion_borrar_obj, opcion_borrar_todo, opcion_borrar_tempo, opcion_borrar_categoria, opcion_modi_habito, opcion_modi_tempo, opcion_modi_categoria, opcion_modi_objetivo, opcion_estadistica_objetivo, opcion_estadistica_resumen, opcion_estadistica_categoria, opcion_estadistica_rachas, opcion_estadistica_habitos, opcion_fusionar_habitos, opcion_fusionar_categorias
from .utilidades import limpiar_pantalla
from .utilidades import ROJO, VERDE, CIAN, GRIS, print_color, normalizar

import tkinter as tk

# se guarda en una variable para luego simplemente mostrarlo en pantalla
volver = f"[ENTER] Cerrar aplicación."
volver2 = f"..............................................."
volver_principal = f"[ENTER] Volver al menú principal."

#menu principal
def mostrar_menu():
    # se repite en bucle hasta que se pulse Salir
    while True:
        limpiar_pantalla()
        habitos = mostrar_registros()
        temporizadores = mostrar_temporizadores()
        categorias = mostrar_categorias()

        print_color("\n======== HABIT TRACKER (FASE BETA v.0.91) ========",VERDE,"\n")
        print_color("1. Añadir un nuevo hábito ",VERDE,"\n")
        if not habitos:
            print_color("2. Registrar tiempo ",GRIS,"\n")2
        else:
            print_color("2. Registrar tiempo ",VERDE,"\n")
        if not habitos and not temporizadores and not categorias:
            print_color("3. Eliminar elementos ",GRIS,"\n")
        else:
            print_color("3. Eliminar elementos ",VERDE,"\n")
        if not habitos and not temporizadores and not categorias:
            print_color("4. Modificar elementos ",GRIS,"\n")
        else:
            print_color("4. Modificar elementos ",VERDE,"\n")
        if not habitos and not temporizadores and not categorias:
            print_color("5. Fusionar elementos ",GRIS,"\n")
        else:
            print_color("5. Fusionar elementos ",VERDE,"\n")
        if not habitos and not temporizadores and not categorias:
            print_color("6. Mostrar estadísticas ",GRIS,"\n")
        else:
            print_color("6. Mostrar estadísticas ",VERDE,"\n")
        print_color("=============================================",VERDE,"\n\n")
        print_color(volver,CIAN,"\n\n")

        opcion = input("Selecciona una opción: ")

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
        print_color("Actualmente no existe ningún elemento a eliminar.",CIAN)
    return True

def opcion_4():
    limpiar_pantalla()
    lista = mostrar_categorias()
    if lista:
        mostrar_menu_modificar()
    else:
        print_color("Actualmente no existe ningún elemento a modificar.",CIAN)
    return True
def opcion_5():
    limpiar_pantalla()
    lista = mostrar_categorias()
    if lista:
        mostrar_menu_fusionar()
    else:
        print_color("Actualmente no existe ningún elemento a fusionar.",CIAN)
    return True
def opcion_6():
    limpiar_pantalla()
    lista = mostrar_categorias()
    if lista:
        mostrar_menu_estadisticas()
    else:
        print_color("Actualmente no existe ningún elemento.",CIAN)
    return True

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
    
    # si la opción escogida está en el diccionario menu, redirige a la opción escogida
    if opcion in menu:
        return menu[opcion]()
    # normaliza tanto volver como salir, y cierra el menú actual
    elif normalizar(opcion) in ("volver","salir",""):
        print_color("Cerrando aplicación...",VERDE)
        return False 
    else:
        return True

#menu borrar    
def mostrar_menu_borrar():
    while True:
        limpiar_pantalla()
        categorias = mostrar_categorias()
        if categorias:
            habitos = mostrar_registros()
            objetivos = mostrar_objetivos()
            temporizadores = mostrar_temporizadores()
            categorias = mostrar_categorias()
            
        # se repite en bucle hasta que se pulse Salir
            print_color("\n========= MENÚ DE BORRADO =========",VERDE,"\n")
            if not habitos:
                print_color("1. Eliminar un hábito ",GRIS,"\n")
            else:
                print_color("1. Eliminar un hábito ",VERDE,"\n")
            if not objetivos:
                print_color("2. Eliminar un objetivo",GRIS,"\n")
            else:
                print_color("2. Eliminar un objetivo ",VERDE,"\n")
            if not temporizadores:
                print_color("3. Eliminar un temporizador",GRIS,"\n")
            else:
                print_color("3. Eliminar un temporizador",VERDE,"\n")

            print_color("4. Eliminar una categoría ",VERDE,"\n")
            print_color("5. Eliminar todos los elementos ",VERDE,"\n")
            print_color("====================================",VERDE)
            print_color(volver_principal,CIAN)

            opcion = input("Selecciona una opción: ")
        else:
            break
        if not borrar(opcion):
            break

# las distintas opciones del menu borrar           
def borrar_1():
    limpiar_pantalla()
    opcion_borrar()
    return True
def borrar_2():
    limpiar_pantalla()
    opcion_borrar_obj()
    return True
def borrar_3():
    limpiar_pantalla()
    opcion_borrar_tempo()
    return True
def borrar_4():
    limpiar_pantalla()
    opcion_borrar_categoria()
    return True
def borrar_5():
    opcion_borrar_todo()
    return True

# diccionario que contiene la redirección de las funciones
menu_borrar = {
    "1": borrar_1,
    "2": borrar_2,
    "3": borrar_3,
    "4": borrar_4,
    "5": borrar_5
}
    
def borrar(opcion):
        # si la opción escogida está en el diccionario menu, redirige a la opción escogida
    if opcion in menu_borrar:
        return menu_borrar[opcion]()
    # normaliza tanto volver como salir, y cierra el menú actual
    elif normalizar(opcion) in ("volver","salir",""):
        return False 
    else:
        return True

def mostrar_menu_modificar():
    while True:
        limpiar_pantalla()
        categorias = mostrar_categorias()
        if categorias:
            habitos = mostrar_registros()
            objetivos = mostrar_objetivos()
            temporizadores = mostrar_temporizadores()
            categorias = mostrar_categorias()
        # se repite en bucle hasta que se pulse Salir
            print_color("\n========= MENÚ DE MODIFICACIÓN =========",VERDE,"\n")
            if not habitos:
                print_color("1. Modificar un hábito",GRIS)
            else:
                print_color("1. Modificar un hábito ",VERDE,"\n")
            if not objetivos:
                print_color("2. Modificar un objetivo",GRIS)
            else:
                print_color("2. Modificar un objetivo ",VERDE,"\n")
            if not temporizadores:
                print_color("3. Modificar un temporizador",GRIS,"\n")
            else:
                print_color("3. Modificar un temporizador ",VERDE,"\n")

            print_color("4. Modificar una categoría ",VERDE,"\n")
            print_color("====================================",VERDE)
            print_color(volver_principal,CIAN)
            
            opcion = input("Selecciona una opción: ")
        else:
            break
        if not modificar(opcion):
            break

# las distintas opciones del menu modificar           
def modi_1():
    limpiar_pantalla()
    opcion_modi_habito()
    return True
def modi_2():
    limpiar_pantalla()
    opcion_modi_objetivo()
    return True
def modi_3():
    temporizadores = mostrar_temporizadores()
    if not temporizadores:
        return True
    else:
        limpiar_pantalla()
        opcion_modi_tempo()
        return True
def modi_4():
    limpiar_pantalla()
    opcion_modi_categoria()
    return True
# diccionario que contiene la redirección de las funciones
menu_modificar = {
    "1": modi_1,
    "2": modi_2,
    "3": modi_3,
    "4": modi_4
}

def modificar(opcion):
    # si el usuario escribe volver o salir también sale de la aplicación
    if opcion == "":
        return False
    # si la opcion coincide con una del diccionario menu_borrar, redirige a esa función
    if opcion in menu_modificar:
        return menu_modificar[opcion]()
    if normalizar(opcion) in ("volver","salir",""):
        print_color("Cerrando aplicación...",VERDE)
        return False
    else:
        limpiar_pantalla()
        print_color("Opción no válida.",ROJO)
        return True

def mostrar_menu_estadisticas():
    while True:
        limpiar_pantalla()
        categorias = mostrar_categorias()
        if categorias:
            habitos = mostrar_registros()
            temporizadores = mostrar_temporizadores()
            categorias = mostrar_categorias()
        # se repite en bucle hasta que se pulse Salir
            print_color("\n========= MENÚ ESTADÍSTICAS =========",VERDE,"\n")
            
            print_color("1. Resumen ",VERDE,"\n")
           
            print_color("2. Categorías ",VERDE,"\n")

            print_color("3. Objetivos ",VERDE,"\n")
            if not temporizadores:
                print_color("4. Constancia ",GRIS,"\n")
            else:
                print_color("4. Constancia ",VERDE,"\n")
            if not temporizadores:
                print_color("5. Hábitos ",GRIS,"\n")
            else:  
                print_color("5. Hábitos ",VERDE,"\n")
            print_color("====================================",VERDE,"\n")
            print_color("\n[ENTER] Volver al menú principal",CIAN,"\n")
            opcion = input("\nSelecciona una opción: ")
        else:
            break
        if not estadisticas(opcion):
            break

# las distintas opciones del menu estadisticas           
def estadisticas_1():
    limpiar_pantalla()
    opcion_estadistica_resumen()
    return True
def estadisticas_2():
    limpiar_pantalla()
    opcion_estadistica_categoria()
    return True
def estadisticas_3():
    limpiar_pantalla()
    opcion_estadistica_objetivo()
    return True
   
def estadisticas_4():
    temporizadores = mostrar_temporizadores()
    if not temporizadores:
        return True
    else:
        limpiar_pantalla()
        opcion_estadistica_rachas()
    return True
def estadisticas_5():
    temporizadores = mostrar_temporizadores()
    if not temporizadores:
        return True
    else:
        limpiar_pantalla()
        opcion_estadistica_habitos()
        return True
# diccionario que contiene la redirección de las funciones
menu_estadisticas = {
    "1": estadisticas_1,
    "2": estadisticas_2,
    "3": estadisticas_3,
    "4": estadisticas_4,
    "5": estadisticas_5
}

def estadisticas(opcion):
    # si el usuario escribe volver o salir también sale de la aplicación
    if normalizar(opcion) in ("volver","salir",""):
        print_color("Volviendo al menú principal...",VERDE)
        return False
    # si la opcion coincide con una del diccionario menu_estadisticas, redirige a esa función

    if opcion in menu_estadisticas:
        return menu_estadisticas[opcion]()
    else:
        limpiar_pantalla()
        print_color("Opción no válida.",ROJO)
        return True

def fusionar(opcion):
    if normalizar(opcion) in ("volver", "salir", ""):
        print_color("Volviendo al menú principal...", VERDE)
        return False

    if opcion in menu_fusionar:
        return menu_fusionar[opcion]()

    limpiar_pantalla()
    print_color("Opción no válida.", ROJO)
    return True

def mostrar_menu_fusionar():
    while True:
        limpiar_pantalla()
       
        print_color("\n========= MENÚ DE FUSIÓN =========",VERDE,"\n")
        print_color("1. Fusionar hábitos ",VERDE,"\n")
        print_color("2. Fusionar categorías ",VERDE,"\n")
        print_color("====================================",VERDE)
        print_color(volver_principal,CIAN)
        opcion = input("Selecciona una opción: ")
        
        if not fusionar(opcion):
            break

# las distintas opciones del menu fusionar           
def fusionar_1():
    limpiar_pantalla()
    opcion_fusionar_habitos()
    return True

def fusionar_2():
    limpiar_pantalla()
    opcion_fusionar_categorias()
    return True


# diccionario que contiene la redirección de las funciones
menu_fusionar = {
    "1": fusionar_1,
    "2": fusionar_2
}   
