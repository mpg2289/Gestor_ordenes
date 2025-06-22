from flask import Flask, render_template, request, redirect, url_for
from ordenes import mostrar_ordenes, cargar_stock
import webbrowser

app = Flask(__name__)#Initialize the flask app


#Pagina principal
@app.route("/", methods=["GET"])
def index():
    ordenes = mostrar_ordenes()
    return render_template("index.html", ordenes=ordenes)

#Pagina de resultados
@app.route("/consultar", methods=["POST"])
def consultar_multiple():
    ordenes_input = request.form["ordenes"]
    ordenes_ids = [o.strip() for o in ordenes_input.replace("\n", ",").split(",") if o.strip()]

    datos_ordenes = mostrar_ordenes()
    stock = cargar_stock()

    resultados = []

    for oid in ordenes_ids:
        articulos = datos_ordenes.get(oid, [])
        total_faltan = 0
        hay_dudosos = False

        for item in articulos:
            articulo = item["articulo"]
            ubicaciones = stock.get(articulo, [])
            total_disponible = sum(u["disponible"] for u in ubicaciones)
            item["estado"] = "ok" if total_disponible >= item["cantidad"] else "falta"

            if any(u["ubicacion"] in ["MONTAJE", "T-CHIC", "VERIFICAR"] for u in ubicaciones):
                hay_dudosos = True
            if item["estado"] == "falta":
                total_faltan += 1

        if not articulos:
            estado_global = "desconocida"
        elif total_faltan > 0:
            estado_global = "no_montable"
        elif hay_dudosos:
            estado_global = "dudosa"
        else:
            estado_global = "montable"

        resultados.append({
            "orden": oid,
            "estado": estado_global
        })

    return render_template("index.html", ordenes=ordenes_ids, resultados=resultados)

#Pagina de detalle
@app.route("/detalle", methods=["POST"])
def consultar_detalle():
    numero_orden = request.form["orden"]
    ordenes = mostrar_ordenes()
    stock = cargar_stock()

    articulos = ordenes.get(numero_orden, [])

    for item in articulos:
        articulo = item["articulo"]
        info_stock = stock.get(articulo, [])

        total_disponible = sum(entry["disponible"] for entry in info_stock)
        item["disponible"] = total_disponible
        item["ubicaciones"] = info_stock

        ubicaciones_criticas = ["MONTAJE", "T-CHIC", "VERIFICAR"]
        item["alerta"] = any(entry["ubicacion"] in ubicaciones_criticas for entry in info_stock)
        item["estado"] = "ok" if total_disponible >= item["cantidad"] else "falta"

    return render_template("resultado.html", orden=numero_orden, ordenes=articulos)


if __name__ == "__main__":
    #webbrowser.open("http://localhost:5000")
    app.run(debug=True)