from flask import Blueprint, request, jsonify

from services.reseñas import (
    crear_reseña_service,
    obtener_reseñas_aprobadas_service,
    obtener_todas_las_reseñas_service,
    modificar_reseña_service, reservas_reseñables_service,
    obtener_mis_reseñas_service
)
from services.verificaciones import check_usuario_es_admin, check_usuario

reseñas_bp = Blueprint(
    "reseñas",
    __name__
)


@reseñas_bp.route("/", methods=["POST"])
def crear_reseña():
    data = request.json
    is_user, error = check_usuario()

    if not is_user:
        respuesta, status = error
        return jsonify(respuesta), status

    respuesta, status = (
        crear_reseña_service(data)
    )

    return jsonify(respuesta), status

@reseñas_bp.route("/reseñables", methods=["GET"])
def obtener_reseñables():
    is_user, error = check_usuario()

    if not is_user:
        respuesta, status = error
        return jsonify(respuesta), status

    return reservas_reseñables_service()

@reseñas_bp.route("/", methods=["GET"])
def obtener_reseñas_aprobadas():
    respuesta, status = (
        obtener_reseñas_aprobadas_service()
    )

    return jsonify(respuesta), status



@reseñas_bp.route("/todas", methods=["GET"])
def obtener_todas_las_reseñas():
    es_admin, error = check_usuario_es_admin()
    if not es_admin:
        respuesta, status = error
        return jsonify(respuesta), status

    respuesta, status = (
        obtener_todas_las_reseñas_service()
    )

    return jsonify(respuesta), status

@reseñas_bp.route("/usuario", methods=["GET"])
def obtener_mis_reseñas():
    is_user, error = check_usuario()
    if not is_user:
        respuesta, status = error
        return jsonify(respuesta), status

    respuesta, status = (
        obtener_mis_reseñas_service()
    )
    print("respuesta:", respuesta)
    return jsonify(respuesta), status

@reseñas_bp.route("/<int:id>", methods=["PATCH"])
def modificar_reseña(id):
    data = request.json

    es_admin, error = check_usuario_es_admin()
    if not es_admin:
        respuesta, status = error
        return jsonify(respuesta), status

    respuesta, status = (
        modificar_reseña_service(
            id,
            data
        )
    )

    return jsonify(respuesta), status