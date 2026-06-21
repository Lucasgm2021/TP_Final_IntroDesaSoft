import uuid

from supabase import create_client
from flask import jsonify

from services.messages import error_msg
from db.imagenes import listar_imagenes as listar_imagenes_db
from db.imagenes import guardar_imagen as guardar_imagenes_db
from services.messages import error_msg
from constants import SUPABASE_URL, SUPABASE_API_KEY, BUCKET_NAME


def subir_imagenes(img, img_name):
    if not img or not img.filename:
        return error_msg(500,"No se recibio archivo.","error")

    try:
        extension = img.filename.split(".")[-1].lower()
        nombre_archivo = f"{uuid.uuid4()}.{extension}"
        contenido = archivo.read()

        client = create_client(SUPABASE_URL,SUPABASE_API_KEY)

        client.storage.from_(BUCKET_NAME).upload(
            path=nombre_archivo,
            file=contenido,
            file_options={"content_type": "image/jpeg"}
        )

    except Exception as error:
        return error_msg(500,"El archivo no existe.","error",Exception)

    guardar_imagenes_db(img,img_name)
    return {"msg":"Imagen subida correctamente"},201


def listar_imagenes():
    return listar_imagenes_db(),200
