from flask import Blueprint, request, jsonify
from services.usuarios import (
    crear_cliente_service,
    crear_usuario_service,
    eliminar_mi_perfil_service,
    obtener_mi_perfil_service,
    obtener_usuarios_service,
    obtener_usuario_email_service,
    actualizar_mi_perfil_service,
    actualizar_usuario_service,
    eliminar_usuario_service
)
from services.verificaciones import check_usuario_es_admin
from services.messages import (error_msg)

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/registro", methods=["POST"]) 
def crear_cliente():
    data= request.get_json()
    if not data:
        return jsonify(error_msg(400, "Body requerido")), 400
    respuesta, status = crear_cliente_service(data)
    return jsonify(respuesta), status


@usuarios_bp.route("/admin", methods=["POST"]) 
def crear_usuario():
    data= request.get_json()
    if not data:
        return jsonify(error_msg(400, "Body requerido")), 400

    #es_admin, error = check_usuario_es_admin()

    #if not es_admin:#no deberia porque pasar
        #respuesta, status = error
        #return jsonify(respuesta), status

    respuesta, status = crear_usuario_service(data)
    return jsonify(respuesta), status

@usuarios_bp.route("/", methods=["GET"])
def obtener_usuarios():
    es_admin, error = check_usuario_es_admin()

    if not es_admin: #no deberia porque pasar
        respuesta, status = error
        return jsonify(respuesta), status

    respuesta, status = obtener_usuarios_service()
    return jsonify(respuesta), status

@usuarios_bp.route("/admin/<string:email>", methods=["GET"])  
def obtener_usuario_email(email):
    #es_admin, error = check_usuario_es_admin()

    #if not es_admin: #no deberia porque pasar
       # respuesta, status = error
        #return jsonify(respuesta), status

    respuesta, status = obtener_usuario_email_service(email)
    return jsonify(respuesta), status

@usuarios_bp.route("/cliente/mi_perfil", methods=["GET"]) 
def obtener_mi_perfil():
    respuesta, status = obtener_mi_perfil_service()
    return jsonify(respuesta), status

@usuarios_bp.route("/cliente/mi_perfil", methods=["PATCH"]) 
def actualizar_mi_perfil():
    data= request.get_json()
    if not data:
        return jsonify(error_msg(400, "Body requerido")), 400

    respuesta, status = actualizar_mi_perfil_service(data)
    return jsonify(respuesta), status

@usuarios_bp.route("/cliente/mi_perfil", methods=["DELETE"]) 
def eliminar_mi_perfil():
    respuesta, status = eliminar_mi_perfil_service()
    return jsonify(respuesta), status

@usuarios_bp.route("/admin", methods=["PUT"])  
def actualizar_usuario():
    data= request.get_json()
    if not data:
        return jsonify(error_msg(400, "Body requerido")), 400

    #es_admin, error = check_usuario_es_admin()

    #if not es_admin: #no deberia porque pasar
        #respuesta, status = error
        #return jsonify(respuesta), status

    respuesta, status = actualizar_usuario_service(data)
    return jsonify(respuesta), status

@usuarios_bp.route("/admin/<string:email>", methods=["DELETE"])  
def eliminar_usuario(email):
    #es_admin, error = check_usuario_es_admin()

    #if not es_admin: #no deberia porque pasar
        #respuesta, status = error
        #return jsonify(respuesta), status

    respuesta, status = eliminar_usuario_service(email)
    return jsonify(respuesta), status