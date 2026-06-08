from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template,redirect, url_for, request, flash, session, make_response
from routes.reservas import reserva_bp
from routes.dashboard import dashboard_bp
from routes.auth import auth_front_bp

from servicesfront.verificaciones import usuario_es_valido
from routes.public import public_bp
from datetime import datetime, timedelta

from datetime import timedelta
from flask import Flask, render_template

from services.inicio import obtener_info_restaurante, obtener_servicios_extra, obtener_reseñas_aprobadas, obtener_menu_publico

app = Flask(__name__)
app.config["SECRET_KEY"] = "mandarina"
app.config["SESSION_PERMANENT"] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)

@app.route("/examples")
def examples():
    return render_template("examples/example.html")

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

app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
app.register_blueprint(auth_front_bp, url_prefix="/auth")
app.register_blueprint(public_bp)
app.register_blueprint(reserva_bp,url_prefix="/reservas")


if __name__ == "__main__":
    app.run(debug=True, port=5000)