from flask import jsonify

from services.messages import error_msg
from db.imagenes import listar_imagenes as listar_imagenes_db
from db.imagenes import guardar_imagen as guardar_imagenes_db



def subir_imagenes(img, name):
    guardar_imagenes_db(name,img)
    return error_msg(200,"Imagen subida correctamente","info")


def listar_imagenes():

    respuesta, code = listar_imagenes_db()
    return respuesta, code