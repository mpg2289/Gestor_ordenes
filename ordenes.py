import json
import os
import sys

import csv

def ruta_relativa(nombre_archivo):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, nombre_archivo)

def mostrar_ordenes():
    ruta = ruta_relativa("ordenes.json")
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)




def cargar_stock():
    path = ruta_relativa("stock.csv")
    stock_dict = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            articulo = row["articulo"]
            try:
                disponible = int(row["disponible"])
            except ValueError:
                continue

            ubicacion = row["ubicacion"]

            entrada = {"disponible": disponible, "ubicacion": ubicacion}

            if articulo in stock_dict:
                stock_dict[articulo].append(entrada)
            else:
                stock_dict[articulo] = [entrada]
    return stock_dict
