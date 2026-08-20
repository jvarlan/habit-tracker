import os
import subprocess

import subprocess


def actualizar_programa():
    try:
        # Actualizar código desde GitHub
        resultado_git = subprocess.run(
            ["git", "pull"],
            capture_output=True,
            text=True
        )

        print(resultado_git.stdout)

        if resultado_git.returncode != 0:
            print("Error al actualizar el programa:")
            print(resultado_git.stderr)
            return False

        # Actualizar/instalar dependencias
        resultado_pip = subprocess.run(
            ["pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True
        )

        print(resultado_pip.stdout)

        if resultado_pip.returncode != 0:
            print("Error al instalar las dependencias:")
            print(resultado_pip.stderr)
            return False

        return True

    except Exception as e:
        print(f"No se pudo actualizar el programa: {e}")
        return False

actualizar_programa()

# Crear la carpeta de datos si no existe
os.makedirs("datos", exist_ok=True)

# Crear los CSV si no existen
archivos_datos = [
    "categorias.csv",
    "habitos.csv",
    "objetivos.csv",
    "temporizadores.csv"
]

for archivo in archivos_datos:
    ruta = os.path.join("datos", archivo)
    if not os.path.exists(ruta):
        open(ruta, "w", encoding="utf-8").close()


from tracker import mostrar_menu


def main():
    # llama al menu principal
    mostrar_menu()


if __name__ == "__main__":
    main()