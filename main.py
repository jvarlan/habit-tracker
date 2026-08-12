import os

# Crear la carpeta de datos si no existe
os.makedirs("datos", exist_ok=True)

from tracker import mostrar_menu


def main():
    # llama al menu principal
    mostrar_menu()


if __name__ == "__main__":
    main()