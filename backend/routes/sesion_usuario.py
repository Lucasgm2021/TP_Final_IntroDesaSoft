from flask import (
    Blueprint,
    request,
    jsonify,
    session
)

from services.sesion_usuario import (
    login_service,
    register_service,
    logout_service
)

sesion_usuario_bp = Blueprint("sesion_usuario",__name__)

@sesion_usuario_bp.route("/login",methods=["POST"])
def login():
    data = request.json
    respuesta, status = login_service(data)
    return jsonify(respuesta), status

#No confundir con crear_usuario de endpoint-usuario,
#este es para registrarse, el otro es para admins
@sesion_usuario_bp.route("/register",methods=["POST"])
def register():
    data = request.json
    respuesta, status = register_service(data)
    return jsonify(respuesta), status

@sesion_usuario_bp.route("/logout",methods=["POST"])
def logout():
    respuesta, status = logout_service()
    return jsonify(respuesta), status


#temp
@sesion_usuario_bp.route("/perfil")
def perfil():
    if "id_usuario" not in session:
        return "No iniciaste sesion"
    return f"""
    <p> Usuario: {session['id_usuario']} </p>
    <p> Email: {session['email']} </p>
    <p> Admin: {True if session['es_admin'] else False} </p>
    """