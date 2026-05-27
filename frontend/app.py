from datetime import timedelta

from flask import Flask, render_template
from flask_cors import CORS

from routes.dashboard import dashboard_bp
from routes.auth import auth_front_bp
app = Flask(__name__)
app.config["SECRET_KEY"] = "mandarina"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)

CORS(app)

@app.route("/examples")
def examples():
    return render_template("examples/example.html")

app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
app.register_blueprint(auth_front_bp, url_prefix="/auth")

if __name__ == "__main__":
    app.run(debug=True)