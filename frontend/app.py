from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template,redirect, url_for, request, flash, session, make_response
from routes.reservas import reserva_bp
from routes.dashboard import dashboard_bp
from routes.auth import auth_front_bp

from services import sesion
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["SECRET_KEY"] = "manzana"
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)

@app.route("/examples")
def examples():
    return render_template("examples/example.html")

@app.route("/")
def inicio():
    error = request.args.get("error",None)
    return render_template("base.html",usuario_logueado=usuario_es_valido(),error=error)

app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
app.register_blueprint(auth_front_bp, url_prefix="/auth")
app.register_blueprint(reserva_bp,url_prefix="/reservas")

if __name__ == "__main__":
    app.run(debug=True)