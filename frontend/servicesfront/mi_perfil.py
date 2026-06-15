from flask import session
import requests
from constants import API_BASE_URL


def obtener_mi_perfil():
    cookie_backend = session.get("usuario") or ""
    try:
        respuesta = requests.get(f"{API_BASE_URL}/usuarios/cliente/mi_perfil", cookies={"session": cookie_backend})
        if respuesta.status_code == 200:
            return respuesta.json()
        return {}
    except requests.RequestException as e:
        return {}


def actualizar_mi_perfil(email, password):
    cookie_backend = session.get("usuario") or ""
    try:
        payload = {
            "nuevo_email": email,
            "nueva_contraseña": password
        }
        respuesta = requests.patch(f"{API_BASE_URL}/usuarios/cliente/mi_perfil", json=payload,
                                   cookies={"session": cookie_backend})
        return respuesta.status_code, respuesta.json()
    except requests.RequestException:
        return 500, {"error": "Error de conexión con el servidor"}


def eliminar_mi_perfil():
    cookie_backend = session.get("usuario") or ""
    try:
        respuesta = requests.delete(f"{API_BASE_URL}/usuarios/cliente/mi_perfil", cookies={"session": cookie_backend})
        return respuesta.status_code
    except requests.RequestException:
        return 500