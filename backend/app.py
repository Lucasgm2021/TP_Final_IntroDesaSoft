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



app = Flask(__name__)

app.config["SECRET_KEY"] = "mandarina"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1234@localhost:3306/restaurante"
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SESSION_SQLALCHEMY_TABLE"] = "sessions"

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
    app.run(debug=True)