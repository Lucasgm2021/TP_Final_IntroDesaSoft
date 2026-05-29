import requests

BACKEND_URL = "http://localhost:5005"


def obtener_info_restaurante():
    try:
        respuesta = requests.get(BACKEND_URL + "/info_frontend")
        respuesta.raise_for_status()
        items = respuesta.json().get("data", [])
        resultado = {}
        for item in items:
            resultado[item["clave"]] = item["valor"]
        return resultado
    except requests.RequestException:
        return {}


def obtener_menu_publico():
    try:
        respuesta = requests.get(BACKEND_URL + "/menu")
        respuesta.raise_for_status()
        return respuesta.json().get("data", [])
    except requests.RequestException:
        return []


def obtener_reseñas_aprobadas():
    try:
        respuesta = requests.get(BACKEND_URL + "/reseñas/")
        respuesta.raise_for_status()
        return respuesta.json().get("data", [])
    except requests.RequestException:
        return []


def obtener_servicios_extra():
    try:
        respuesta = requests.get(BACKEND_URL + "/servicios_extra")
        respuesta.raise_for_status()
        return respuesta.json().get("data", [])
    except requests.RequestException:
        return []