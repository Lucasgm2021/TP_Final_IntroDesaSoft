from dotenv import load_dotenv
import os

# If the hidden Docker file DOES NOT exist, we are running natively in the terminal
if not os.path.exists('/.dockerenv'):
    print("Running natively: Loading local .env file...")
    load_dotenv()
else:
    print("Running inside Docker: Using container injected environment...")

from routes.reservas import reserva_bp
from routes.dashboard import dashboard_bp
from routes.auth import auth_front_bp
from routes.reseñas import reseñas_front_bp

from servicesfront.verificaciones import usuario_es_valido
from routes.public import public_bp
from datetime import timedelta
from flask import Flask, render_template
from servicesfront.inicio import obtener_info_restaurante, obtener_servicios_extra, obtener_reseñas_aprobadas, obtener_menu_publico
from servicesfront.verificaciones import usuario_es_valido, usuario_es_admin

from routes.mi_perfil import usuarios_bp
app = Flask(__name__)
app.config["SECRET_KEY"] = "mandarina"
app.config["SESSION_PERMANENT"] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)



@app.route("/")
def inicio():
    user = usuario_es_valido()
    info = obtener_info_restaurante()
    admin = usuario_es_admin()
    menu = obtener_menu_publico()
    reseñas = obtener_reseñas_aprobadas()
    servicios = obtener_servicios_extra()

    return render_template(
        "inicio/inicio.html",
        usuario_logueado=user,
        usuario_admin=admin,
        info=info,
        menu=menu,
        reseñas=reseñas,
        servicios=servicios,
    )

app.register_blueprint(reseñas_front_bp, url_prefix="/reseñas")
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
app.register_blueprint(auth_front_bp, url_prefix="/auth")
app.register_blueprint(public_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(reserva_bp,url_prefix="/reservas")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)