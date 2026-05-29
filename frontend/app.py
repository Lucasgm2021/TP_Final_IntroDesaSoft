from datetime import timedelta
from flask import Flask, render_template

from services.inicio import obtener_info_restaurante
from services.inicio import obtener_menu_publico
from services.inicio import obtener_reseñas_aprobadas
from services.inicio import obtener_servicios_extra

app = Flask(__name__)
app.config["SECRET_KEY"] = "mandarina"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)


@app.route("/")
def inicio():
    info = obtener_info_restaurante()
    menu = obtener_menu_publico()
    reseñas = obtener_reseñas_aprobadas()
    servicios = obtener_servicios_extra()
    return render_template(
        "inicio/inicio.html",
        info=info,
        menu=menu,
        reseñas=reseñas,
        servicios=servicios,
    )


@app.route("/examples")
def examples():
    return render_template("examples/example.html")


if __name__ == "__main__":
    app.run(debug=True)