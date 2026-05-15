from flask import Blueprint, request, jsonify

from services.reseñas import (
    crear_reseña_service,
    obtener_reseñas_aprobadas_service,
    obtener_todas_las_reseñas_service

)

reseñas_bp = Blueprint(
    "reseñas",
    __name__
)


@reseñas_bp.route("/", methods=["POST"])
def crear_reseña():
    data = request.json

    respuesta, status = (
        crear_reseña_service(data)
    )

    return jsonify(respuesta), status

@reseñas_bp.route("/", methods=["GET"])
def obtener_reseñas_aprobadas():
    respuesta, status = (
        obtener_reseñas_aprobadas_service()
    )

    return jsonify(respuesta), status


#al tener admin deberia comprobar que sea admin, pero como no tenemos sessions todavia
#lo dejo asi para determinar que es para admins
@reseñas_bp.route("/admin", methods=["GET"])
def obtener_todas_las_reseñas():
    respuesta, status = (
        obtener_todas_las_reseñas_service()
    )

    return jsonify(respuesta), status