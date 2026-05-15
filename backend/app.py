from flask import Flask
#from routes.usuarios import usuarios_bp
#from routes.menu import menu_bp
#from routes.reservas import reservas_bp
from routes.reseñas import reseñas_bp
#from routes.info_frontend import info_frontend_bp
#from routes.estadisticas import estadisticas_bp

app = Flask(__name__)

app.json.sort_keys = False

@app.route("/")
def index():
    return "hola mundo!"

#app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
#app.register_blueprint(menu_bp, url_prefix="/menu")
#app.register_blueprint(reservas_bp, url_prefix="/reservas")
app.register_blueprint(reseñas_bp, url_prefix="/reseñas")
#app.register_blueprint(info_frontend_bp, url_prefix="/info_frontend")
#app.register_blueprint(estadisticas_bp, url_prefix="/estadisticas")

if __name__ == "__main__":
    app.run(debug=True, port=5554)
