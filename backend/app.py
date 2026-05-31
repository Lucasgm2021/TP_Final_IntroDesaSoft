from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

from datetime import timedelta
from routes.usuarios import usuarios_bp
from routes.menu import menu_bp
from routes.reservas import reservas_bp
from routes.reseñas import reseñas_bp
from routes.info_frontend import info_frontend_bp
from routes.sesion_usuario import sesion_usuario_bp
#from routes.estadisticas import estadisticas_bp
from routes.mesas import mesas_bp
from flask_cors import CORS

# 2. Relax cookie security rules for local cross-port development
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = False  # Keep False because we are using HTTP, not HTTPS
"""

app = Flask(__name__)
# 1. Restrict origins to your frontend port and enable credentials (cookies)
CORS(app, origins=["http://localhost:5001"], supports_credentials=True)

# 2. Tell the browser it's allowed to send this Session ID cookie across ports
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False  # Keep False for HTTP localhost development

app.config["SECRET_KEY"] = "mandarina"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1234@localhost:3306/restaurante"
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SESSION_SQLALCHEMY_TABLE"] = "sessions"
# Inside your BACKEND app configuration file:
app.config["SESSION_COOKIE_NAME"] = "backend_session"

app.json.sort_keys = False

db = SQLAlchemy(app)

app.config["SESSION_SQLALCHEMY"] = db

Session(app)
CORS(app)


@app.route("/")
def index():
    return "Backend encendido"


app.register_blueprint(mesas_bp, url_prefix="/mesas")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
app.register_blueprint(menu_bp, url_prefix="/menu")
app.register_blueprint(reseñas_bp, url_prefix="/reseñas")
app.register_blueprint(info_frontend_bp, url_prefix="/info_frontend")
app.register_blueprint(sesion_usuario_bp, url_prefix="/sesion")
app.register_blueprint(reservas_bp, url_prefix="/reservas")

if __name__ == "__main__":
    app.run(debug=True,port=5005)