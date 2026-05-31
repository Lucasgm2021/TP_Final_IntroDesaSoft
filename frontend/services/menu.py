import requests

BACKEND_URL = "http://localhost:5005"


def obtener_menu():
    # Pide el menu completo al backend (endpoint publico, sin sesion).
    # Devuelve la lista de platos (dicts). Si el backend no responde,
    # devuelve lista vacia para que la pagina no rompa.
    try:
        respuesta = requests.get(f"{BACKEND_URL}/menu")
        respuesta.raise_for_status()
        return respuesta.json().get("data", [])
    except requests.RequestException:
        return []
