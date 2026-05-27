from flask import session
import requests

def usuario_es_valido():
    data = session.get("usuario") or ''

    sesion = requests.get(
        f'http://localhost:5005/sesion/perfil',
        cookies={'session': data }
    )

    if sesion.status_code == 200:
        return True
    else:
        return False

def usuario_es_admin():
    data = session.get("usuario") or ''

    sesion = requests.get(
        f'http://localhost:5005/sesion/perfil',
        cookies={'session': data }
    )

    if sesion.status_code == 200 and sesion.json()["admin"]:
        return True
    else:
        return False