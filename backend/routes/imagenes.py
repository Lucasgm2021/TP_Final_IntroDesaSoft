from flask import Blueprint, request, jsonify

from services.imagenes import subir_imagenes, listar_imagenes
from services.verificaciones import check_usuario_es_admin

imagenes_bp = Blueprint(
    "imagenes",
    __name__
)

@imagenes_bp.route("/upload-img/<string:img_name>", methods=["POST"])
def upload_img(img_name):
    img = request.files["imagen"]

    es_admin, error = check_usuario_es_admin()

    if not es_admin:
        respuesta, status = error
        return jsonify(respuesta), status
    respuesta, status = subir_imagenes(img,img_name)

    return jsonify(respuesta),status

@imagenes_bp.route("/", methods=["GET"])
def listar_img():
    es_admin, error = check_usuario_es_admin()

    if not es_admin:
        respuesta, status = error
        return jsonify(respuesta), status
    respuesta, status = listar_imagenes()
    return respuesta, status