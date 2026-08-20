import os
import subprocess


def actualizar_programa():
    try:
        resultado = subprocess.run(
            ["git", "pull"],
            capture_output=True,
            text=True
        )

        print(resultado.stdout)

        if resultado.returncode != 0:
            print("Error al actualizar el programa:")
            print(resultado.stderr)

    except Exception as e:
        print(f"No se pudo ejecutar git pull: {e}")

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