import requests
from constants import API_BASE_URL, BACKEND_SESSION_COOKIE_NAME
from servicesfront.utiles import leer_respuesta_request

# Reservas

def obtener_todas_las_reservas(auth):
    r = requests.get(
        f"{API_BASE_URL}/reservas/",
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )
    return r.json().get("reservas", [])


# Reseñas

def obtener_todas_las_reseñas(auth):
    r = requests.get(
        f"{API_BASE_URL}/reseñas/todas",
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )
    return r.json().get("data", [])


def aprobar_reseña(id_reseña, auth):
    requests.patch(
        f"{API_BASE_URL}/reseñas/{id_reseña}",
        json={"estado": "aprobada"},
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )


def desaprobar_reseña(id_reseña, auth):
    requests.patch(
        f"{API_BASE_URL}/reseñas/{id_reseña}",
        json={"estado": "no_aprobada"},
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )


# Menu

def obtener_menu():
    r = requests.get(f"{API_BASE_URL}/menu")
    return r.json().get("data", [])


def obtener_plato(id_plato, auth):
    r = requests.get(
        f"{API_BASE_URL}/menu/{id_plato}",
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )
    return r.json().get("data")


def crear_plato(body, auth):
    requests.post(
        f"{API_BASE_URL}/menu",
        json=body,
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )


def editar_plato(id_plato, body, auth):
    requests.put(
        f"{API_BASE_URL}/menu/{id_plato}",
        json=body,
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )


def eliminar_plato(id_plato, auth):
    requests.delete(
        f"{API_BASE_URL}/menu/{id_plato}",
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )


def build_body_plato(form):
    return {
        "nombre":          form.get("nombre"),
        "precio":          int(float(form.get("precio", 0))),
        "id_categoria":    int(form.get("id_categoria", 0)),
        "link_imagen":     form.get("link_imagen") or "",
        "hay_stock":       "hay_stock"       in form,
        "gluten":          "gluten"          in form,
        "producto_animal": "producto_animal" in form,
        "carnes":          "carnes"          in form,
        "lactosa":         "lactosa"         in form,
    }


# Info frontend - Configuración

def obtener_info_frontend(auth):
    r = requests.get(
        f"{API_BASE_URL}/info_frontend",
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )
    return r.json().get("data", [])


def obtener_info_frontend_por_clave(clave, auth):
    r = requests.get(
        f"{API_BASE_URL}/info_frontend/{clave}",
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )
    valor = r.json().get(clave)
    if valor is None:
        return None
    return {"clave": clave, "valor": valor}


def crear_info_frontend(body, auth):
    requests.post(
        f"{API_BASE_URL}/info_frontend",
        json=body,
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )


def editar_info_frontend(clave_original, body, auth):
    requests.patch(
        f"{API_BASE_URL}/info_frontend/{clave_original}",
        json=body,
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )


def eliminar_info_frontend(clave, auth):
    requests.delete(
        f"{API_BASE_URL}/info_frontend/{clave}",
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )


# Usuarios
def obtener_usuarios(auth):
    r = requests.get(
        f"{API_BASE_URL}/usuarios",
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )
    return r.json().get("data", [])


def build_body_usuario(form):
    body = {
        "email":    form.get("email"),
        "es_admin": "es_admin" in form,
    }
    password = form.get("password")
    if password:
        body["password"] = password
    return body


# Mesas
def obtener_mesas(auth):
    r = requests.get(
        f"{API_BASE_URL}/mesas",
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )
    return r.json().get("data", [])


def obtener_mesa(id_mesa, auth):
    r = requests.get(
        f"{API_BASE_URL}/mesas/{id_mesa}",
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )
    return r.json().get("data")


def crear_mesa(body, auth):
    requests.post(
        f"{API_BASE_URL}/mesas",
        json=body,
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )


def editar_mesa(id_mesa, body, auth):
    requests.patch(
        f"{API_BASE_URL}/mesas/{id_mesa}",
        json=body,
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )


def eliminar_mesa(id_mesa, auth):
    requests.delete(
        f"{API_BASE_URL}/mesas/{id_mesa}",
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )


def build_body_mesa(form):
    return {
        "numero":     int(form.get("numero", 0)),
        "capacidad":  int(form.get("capacidad", form.get("comensales", 0))),
        "interior":   1 if "interior"  in form else 0,
        "funcional":  1 if "funcional" in form else 0,
    }


def subir_imagen(imagen,nombre, auth):
    requests.post(
        f"{API_BASE_URL}/imagenes/upload-img/{nombre}",
        files={"imagen": (imagen.filename,imagen.read(),imagen.content_type)},
        cookies={BACKEND_SESSION_COOKIE_NAME: auth
        }
    )

def listar_imagenes(auth):
    try:
        response = requests.get(f"{API_BASE_URL}/imagenes",cookies={BACKEND_SESSION_COOKIE_NAME: auth})
        return leer_respuesta_request(response,200,json=True)
    except requests.exceptions.ConnectionError:
        return {'errores': ['No se pudo conectar con el servidor.']}
    except:
        return {'errores': ['Ocurrió un error inesperado al obtener imagenes. Inténtalo de nuevo más tarde.']}