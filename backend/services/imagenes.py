import uuid

from supabase import create_client
from flask import jsonify

from services.messages import error_msg
from db.imagenes import listar_imagenes as listar_imagenes_db
from db.imagenes import guardar_imagen as guardar_imagenes_db
from services.messages import error_msg
from constants import SUPABASE_URL, SUPABASE_API_KEY, BUCKET_NAME


def subir_imagenes(img_file, img_name):
    if not img_file or not img_file.filename:
        return error_msg(500,"No se recibio archivo.","error")

    try:
        extension = img_file.filename.split(".")[-1].lower()
        nombre_archivo = f"{uuid.uuid4()}.{extension}"
        contenido = img_file.read()

        client = create_client(SUPABASE_URL,SUPABASE_API_KEY)

        client.storage.from_(BUCKET_NAME).upload(
            path=nombre_archivo,
            file=contenido,
            file_options={"content_type": "image/jpeg"}
        )

    except:
        return error_msg(500,"Error al subir la imagen.","")
    
    try:
        url_img = client.storage.from_(BUCKET_NAME).get_public_url(nombre_archivo)
        guardar_imagenes_db(img_name,url_img)
    except:
        return error_msg(500,"Error al guardar la url de la imagen en la bbdd.","")
    return {"msg":"Imagen subida correctamente"},201


def listar_imagenes():
    try:
        imagenes = listar_imagenes_db()
    except: 
        return error_msg(500,"Error obteniendo imagenes",description="Ha ocurrido un error en el servidor.")
    return imagenes,200