from flask import session
import requests

def usuario_es_valido():
    data = session.get("usuario") or ''

    sesion = requests.get(
        f'http://localhost:5000/sesion/perfil',
        cookies={'backend_session': data }
    )

    if sesion.status_code == 200:
        return True
    else:
        return False

def usuario_es_admin():
    data = session.get("usuario") or ''

    sesion = requests.get(
        f'http://localhost:5000/sesion/perfil',
        cookies={'backend_session': data }
    )
    
    if sesion.status_code == 200 and sesion.json()["es_admin"]:
        return True
    else:
        return False