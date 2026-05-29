from datetime import timedelta
from flask import Flask, render_template, request

from routes.dashboard import dashboard_bp
from routes.auth import auth_front_bp

from servicesfront.verificaciones import usuario_es_valido
app = Flask(__name__)
app.config["SECRET_KEY"] = "mandarina"
app.config["SESSION_PERMANENT"] = True
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

if __name__ == "__main__":
    app.run(debug=True)