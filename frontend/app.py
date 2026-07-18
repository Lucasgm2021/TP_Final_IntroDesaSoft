import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, render_template

# Si este archivo de docker no existe (se crea automatico en el contenedor), se cargan las variables de entorno.
if not os.path.exists('/.dockerenv'):
    print("Ejecutando con terminal, cargando las variables de entorno...")
    load_dotenv()
else:
    print("Ejecutando con docker, se cargan las variables de entorno en el yml.")

from routes.reservas import reserva_bp
from routes.dashboard import dashboard_bp
from routes.auth import auth_bp
from routes.reseñas import reseñas_front_bp
from routes.menu import menu_bp
from routes.mi_perfil import usuarios_bp
from routes.home import home_bp
from constants import BASE_URL_FRONT

app = Flask(__name__)
app.config["SECRET_KEY"] = "mandarina"
app.config["SESSION_PERMANENT"] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)

app.register_blueprint(home_bp, url_prefix=f"/{BASE_URL_FRONT}/")
app.register_blueprint(reseñas_front_bp, url_prefix=f"/{BASE_URL_FRONT}/reseñas")
app.register_blueprint(dashboard_bp, url_prefix=f"/{BASE_URL_FRONT}/dashboard")
app.register_blueprint(auth_bp, url_prefix=f"/{BASE_URL_FRONT}/auth")
app.register_blueprint(menu_bp, url_prefix=f"/{BASE_URL_FRONT}/menu")
app.register_blueprint(usuarios_bp,url_prefix=f"/{BASE_URL_FRONT}/usuarios")
app.register_blueprint(reserva_bp,url_prefix=f"/{BASE_URL_FRONT}/reservas")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)