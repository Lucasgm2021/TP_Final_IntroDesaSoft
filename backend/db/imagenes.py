import uuid

from supabase import create_client

from constants import SUPABASE_URL, SUPABASE_API_KEY, BUCKET_NAME
from services.messages import error_msg
from db.config import ejecutar_query_lectura, ejecutar_query_escritura

def listar_imagenes(): #lista todas las imagenes
    query = """
        SELECT *
        FROM imagenes
    """
    resultado = ejecutar_query_lectura(query)

    return [dict(r) for r in resultado],200

def guardar_imagen(name, archivo): #admin: sube una nueva imagen
    if not archivo or not archivo.filename:
        return error_msg(500,"No se recibio archivo.","error")

    try:
        extension = archivo.filename.split(".")[-1].lower()
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


    query = """
        INSERT INTO imagenes (unique_name,img_url)
        VALUES (:name,:url)
    """
    return ejecutar_query_escritura(query, {
        "name": name,
        "url": client.storage.from_(BUCKET_NAME).get_public_url(nombre_archivo)
    })
