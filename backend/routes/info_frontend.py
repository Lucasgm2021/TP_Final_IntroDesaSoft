from flask import Blueprint,request,jsonify

from services.info_frontend import (
    crear_info_service,
    obtener_info_service,
    obtener_info_por_clave_service,
    actualizar_info_service,
    borrar_info_service
)
from services.verificaciones import check_usuario_es_admin

info_frontend_bp = Blueprint(
    "info_frontend",
    __name__
)

@info_frontend_bp.route("/",methods=["POST"])
def crear_info():
    data = request.json
    es_admin, error = check_usuario_es_admin()

    if not es_admin:
        respuesta, status = error
        return jsonify(respuesta), status

    respuesta, status = crear_info_service(data)

    return jsonify(respuesta), status


@info_frontend_bp.route("/",methods=["GET"])
def obtener_info():
    respuesta, status = (
        obtener_info_service()
    )
    return jsonify(respuesta), status


@info_frontend_bp.route("/<string:clave>",methods=["GET"])
def obtener_info_por_clave(clave):
    respuesta, status = (
        obtener_info_por_clave_service(
            clave
        )
    )

    return jsonify(respuesta), status


@info_frontend_bp.route("/<string:clave>",methods=["PATCH"])
def actualizar_info(clave):
    data = request.json
    es_admin, error = check_usuario_es_admin()

    if not es_admin:
        respuesta, status = error

        return jsonify(respuesta), status

    respuesta, status = actualizar_info_service(clave,data)

    return jsonify(respuesta), status

@info_frontend_bp.route("/<string:clave>",methods=["DELETE"])
def borrar_info(clave):
    es_admin, error = check_usuario_es_admin()

    if not es_admin:
        respuesta, status = error
        return jsonify(respuesta), status

    respuesta, status = borrar_info_service(clave)
    return jsonify(respuesta), status
