import requests
from constants import API_BASE_URL


def obtener_mi_perfil(cookies):
    try:
        respuesta = requests.get(f"{API_BASE_URL}/usuarios/cliente/mi_perfil", cookies=cookies)
        if respuesta.status_code == 200:
            return respuesta.json()
        return {}
    except requests.RequestException as e:
        return {}


def actualizar_mi_perfil(email, password,cookies):
    try:
        payload = {
            "nuevo_email": email,
            "nueva_contraseña": password
        }
        respuesta = requests.patch(f"{API_BASE_URL}/usuarios/cliente/mi_perfil", json=payload,
                                   cookies=cookies)
        return respuesta.json()
    except requests.RequestException:
        return {"errores": "Error de conexión con el servidor"}
    except:
        return {'errores': ['Ocurrió un error inesperado al actualizar el perfil. Inténtalo de nuevo más tarde.']}


def eliminar_mi_perfil(cookies):
    try:
        respuesta = requests.delete(f"{API_BASE_URL}/usuarios/cliente/mi_perfil", cookies=cookies)
        return {"message":"ok"}
    except requests.RequestException:
        return {"errores": "Error de conexión con el servidor"}