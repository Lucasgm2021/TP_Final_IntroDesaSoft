import requests, json
from constants import API_BASE_URL

def obtener_info_restaurante():
    try:
        respuesta = requests.get(API_BASE_URL + "/info_frontend")
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
        respuesta = requests.get(API_BASE_URL + "/menu")
        respuesta.raise_for_status()
        return respuesta.json().get("data", [])
    except requests.RequestException:
        return []


def obtener_reseñas_aprobadas():
    try:
        respuesta = requests.get(API_BASE_URL + "/reseñas/")
        respuesta.raise_for_status()
        return respuesta.json().get("data", [])
    except requests.RequestException:
        return []

def obtener_servicios_extra():
    info = obtener_info_restaurante()
    servicios = info.get("servicios_extra", "[]")

    if isinstance(servicios, str):
        try:
            servicios = json.loads(servicios)
        except json.JSONDecodeError:
            return []

    return servicios