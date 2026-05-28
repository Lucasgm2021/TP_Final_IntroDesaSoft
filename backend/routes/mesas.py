from flask import Blueprint, request, jsonify
from services import mesas as servicios_mesas
from services.verificaciones import check_usuario_es_admin

mesas_bp = Blueprint("mesas", __name__)


@mesas_bp.route("/", methods=["GET"])
def obtener_mesas():
    res, status = servicios_mesas.obtener_mesas_service()
    return jsonify(res), status

@mesas_bp.route("/validacion", methods=["GET"])
def obtener_mesas_validas():
    data = {}
    data["fecha"] = request.args.get("fecha")
    data["hora_reserva"] = request.args.get("hora")
    data["interior"] = request.args.get("interior")
    res, status = servicios_mesas.obtener_mesas_validas_service(data)
    return jsonify(res), status

@mesas_bp.route("/<int:id_mesa>", methods=["GET"])
def obtener_mesa(id_mesa):
    res, status = servicios_mesas.obtener_mesa_service(id_mesa)
    return jsonify(res), status

@mesas_bp.route("/", methods=["POST"])
def crear_mesa():
    es_admin, error = check_usuario_es_admin()

    if not es_admin:
        respuesta, status = error
        return jsonify(respuesta), status

    data = request.get_json()
    res, status = servicios_mesas.crear_mesa_service(data)
    return jsonify(res), status

@mesas_bp.route("/<int:id_mesa>", methods=["PATCH"])
def modificar_mesa(id_mesa):
    es_admin, error = check_usuario_es_admin()

    if not es_admin:
        respuesta, status = error
        return jsonify(respuesta), status

    data = request.get_json()
    res, status = servicios_mesas.modificar_mesa_service(id_mesa, data)
    return jsonify(res), status

@mesas_bp.route("/<int:id_mesa>", methods=["DELETE"])
def eliminar_mesa(id_mesa):
    es_admin, error = check_usuario_es_admin()

    if not es_admin:
        respuesta, status = error
        return jsonify(respuesta), status

    res, status = servicios_mesas.eliminar_mesa_service(id_mesa)
    return jsonify(res), status