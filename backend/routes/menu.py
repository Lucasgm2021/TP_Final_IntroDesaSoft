from flask import Blueprint, request, jsonify
from services.menu import (
    obtener_menu_service,
    obtener_plato_service,
    crear_plato_service,
    modificar_plato_service,
    borrar_plato_service
)
from services.verificaciones import check_usuario_es_admin #sessions

menu_bp = Blueprint('menu_bp', __name__)

@menu_bp.route('/', methods=['GET']) # obtiene la lista completa
def obtener_menu():
    respuesta, status = obtener_menu_service()
    return jsonify(respuesta), status

@menu_bp.route('/<int:id_plato>', methods=['GET']) # obtiene un solo plato
def obtener_plato(id_plato):
    respuesta, status = obtener_plato_service(id_plato)
    return jsonify(respuesta), status

@menu_bp.route('/admin', methods=['POST']) #admin: crea un plato nuevo
def agregar_plato():
    es_admin, error = check_usuario_es_admin()
    if not es_admin:
        respuesta, status = error
        return jsonify(respuesta), status

    data = request.json
    respuesta, status = crear_plato_service(data)
    return jsonify(respuesta), status

@menu_bp.route('/admin/<int:id_plato>', methods=['PUT']) #admin: modifica un plato
def editar_plato(id_plato):
    es_admin, error = check_usuario_es_admin()
    if not es_admin:
        respuesta, status = error
        return jsonify(respuesta), status

    data = request.json
    respuesta, status = modificar_plato_service(id_plato, data)
    return jsonify(respuesta), status

@menu_bp.route('/admin/<int:id_plato>', methods=['DELETE']) #admin: borra un plato
def eliminar_plato(id_plato):
    es_admin, error = check_usuario_es_admin()
    if not es_admin:
        respuesta, status = error
        return jsonify(respuesta), status

    respuesta, status = borrar_plato_service(id_plato)
    return jsonify(respuesta), status