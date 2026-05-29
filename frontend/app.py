from datetime import timedelta
from flask import Flask, render_template

from routes.dashboard import dashboard_bp
from routes.auth import auth_front_bp
from routes.public import public_bp
app = Flask(__name__)
app.config["SECRET_KEY"] = "mandarina"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)



@app.route("/examples")
def examples():
    return render_template("examples/example.html")

@app.route("/")
def inicio():
    return render_template("base.html")

app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
app.register_blueprint(auth_front_bp, url_prefix="/auth")
app.register_blueprint(public_bp)

if __name__ == "__main__":
    app.run(debug=True)