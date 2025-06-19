from flask import Flask, render_template, request, redirect, url_for
from ordenes import mostrar_ordenes, cargar_stock
import webbrowser

app = Flask(__name__)

@app.route("/")
def index():
    ordenes = mostrar_ordenes()
    return render_template("index.html", ordenes=ordenes)


@app.route("/consultar", methods=["POST"])
def consultar():
    numero_orden = request.form["orden"]
    ordenes = mostrar_ordenes()
    stock = cargar_stock()

    articulos = ordenes.get(numero_orden, [])

     # Añadir datos de stock a cada artículo
    for item in articulos:
        articulo = item["articulo"]
        info_stock = stock.get(articulo,[])

        if info_stock:
            total_disponible = sum(entry["disponible"] for entry in info_stock)
            item["disponible"] = total_disponible
            item["ubicaciones"] = info_stock 
             # esto es una lista de ubicaciones
            
            ubicaciones_criticas = ["MONTAJE", "T-CHIC", "VERIFICAR"]
            item["alerta"] = any(entry["ubicacion"] in ubicaciones_criticas for entry in info_stock)

            
            item["estado"] = "ok" if item["disponible"] >= item["cantidad"] else "falta"
        else:
            item["disponible"] = 0
            item["ubicacion_stock"] = "Sin datos"
            item["estado"] = "desconocido"
            item["alerta"] = True

    return render_template("index.html", ordenes=articulos, numero_orden=numero_orden)

if __name__ == "__main__":
    #webbrowser.open("http://localhost:5000")
    app.run(debug=True)