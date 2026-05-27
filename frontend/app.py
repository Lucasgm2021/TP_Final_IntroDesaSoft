from flask import Flask, render_template
from flask_cors import CORS

from routes.dashboard import dashboard_bp
app = Flask(__name__)

CORS(app)

@app.route("/examples")
def examples():
    return render_template("examples/example.html")

app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

if __name__ == "__main__":
    app.run(debug=True)