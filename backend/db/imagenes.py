from db.config import ejecutar_query_lectura, ejecutar_query_escritura

def listar_imagenes(): #lista todas las imagenes
    query = """
        SELECT *
        FROM imagenes
    """
    resultado = ejecutar_query_lectura(query)

    return [dict(r) for r in resultado]

def guardar_imagen(img_name,url): #admin: sube una nueva imagen
    query = """
        INSERT INTO imagenes (unique_name,img_url)
        VALUES (:name,:url)
    """
    ejecutar_query_escritura(query, {
        "name": img_name,
        "url": url
    })
