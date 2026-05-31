from flask import session
import requests
from constants import API_BASE_URL,SESSION_COOKIE_NAME, FRONTEND_SESSION

def usuario_es_valido():
    data = session.get(FRONTEND_SESSION) or ''

    sesion = requests.get(
        f'{API_BASE_URL}/sesion/perfil',
        cookies={SESSION_COOKIE_NAME: data }
    )

    if sesion.status_code == 200:
        return True
    else:
        return False

def usuario_es_admin():
    data = session.get(FRONTEND_SESSION) or ''

    sesion = requests.get(
        f'{API_BASE_URL}/sesion/perfil',
        cookies={SESSION_COOKIE_NAME: data }
    )
    
    if sesion.status_code == 200 and sesion.json()["es_admin"]:
        return True
    else:
        return False