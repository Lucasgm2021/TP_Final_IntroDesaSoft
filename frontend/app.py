from flask import Flask, render_template
from flask_cors import CORS
from routes.reservas import reserva_bp

app = Flask(__name__)

CORS(app)

@app.route("/examples")
def index():
    return render_template("examples/example.html")

app.register_blueprint(reserva_bp,url_prefix="/reservas")

if __name__ == "__main__":
    app.run(debug=True)