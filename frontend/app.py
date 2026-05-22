from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route("/examples")
def index():
    return render_template("examples/example.html")

if __name__ == "__main__":
    app.run(debug=True)