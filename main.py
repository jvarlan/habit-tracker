import os

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