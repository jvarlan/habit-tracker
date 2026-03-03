import csv
from config import BASE_DIR
from pathlib import Path
from .checks import comprobar_categoria
from .contar import contar_id

def habito(id_habito,nombre, tiempo, fecha):
    ruta = BASE_DIR / "datos" / "temporizadores.csv"
    ruta.parent.mkdir(exist_ok=True)

    encabezado = not ruta.exists() or ruta.stat().st_size == 0
    id = contar_id("temporizadores.csv")
    with open(ruta, mode="a", newline="", encoding="utf-8") as archivo:
        campos = ["id","id_habito","temporizador", "tiempo", "fecha"]
        writer = csv.DictWriter(archivo, fieldnames=campos)

        if encabezado:
            writer.writeheader()
        writer.writerow({"id": id,"id_habito":id_habito,"temporizador": nombre, "tiempo": tiempo, "fecha": fecha})

def registrar(habito, id_categoria, objetivo):
    
    ruta = BASE_DIR / "datos" / "habitos.csv"
    ruta.parent.mkdir(exist_ok=True)

    encabezado = not ruta.exists() or ruta.stat().st_size == 0

    id = contar_id("habitos.csv")

    with open(ruta, mode="a", newline="",encoding="utf-8") as archivo:
        campos = ["id","habito","id_categoria","objetivo"]
        writer = csv.DictWriter(archivo, fieldnames=campos)

        if encabezado:
            writer.writeheader()
        writer.writerow({"id": id, "habito": habito, "id_categoria": id_categoria, "objetivo": objetivo})

def registrar_categoria(categoria):

    ruta = BASE_DIR / "datos" / "categorias.csv"
    ruta.parent.mkdir(exist_ok=True)

    encabezado = not ruta.exists() or ruta.stat().st_size == 0

    id = contar_id("categorias.csv")

    with open(ruta, mode="a", newline="", encoding="utf-8") as archivo:
        campos = ["id","categoria"]
        writer = csv.DictWriter(archivo, fieldnames=campos)

        if encabezado:
            writer.writeheader()
        if not comprobar_categoria(categoria) >= 1:
            writer.writerow({"id": id,"categoria": categoria}) 
           
    

   
