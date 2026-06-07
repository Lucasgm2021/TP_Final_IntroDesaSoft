from flask import (Blueprint, render_template)
import requests
from constants import API_BASE_URL, BACKEND_SESSION_COOKIE_NAME, FRONTEND_COOKIE_CLAVE

reseñas_front_bp = Blueprint('reseñas_front', __name__)

@reseñas_front_bp.route("/", methods=["GET"])
def mostrar_reseñas():
    try:
        respuesta = requests.get(f"{API_BASE_URL}/reseñas")

        if respuesta.status_code == 200:
            lista_de_reseñas = respuesta.json()["data"]
        else:
            lista_de_reseñas = []
    except requests.exceptions.RequestException:
        lista_de_reseñas = []

    return render_template("reseñas/lista_reseñas.html", reseñas=lista_de_reseñas)