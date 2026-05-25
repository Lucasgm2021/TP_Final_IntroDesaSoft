import requests
from flask import request, redirect, url_for

API_BASE_URL = "http://localhost:5000"

def login(email,password):
    data = {}
    try:
        backend_res = requests.post(f"{API_BASE_URL}/sesion/login",json={
            "email": email,
            "password": password
        }, timeout=10)
        print("respuesta de backend:",backend_res,backend_res.status_code,"cookies:",backend_res.cookies.items())
        if backend_res.status_code == 201:
            cookies_dict = backend_res.cookies.get_dict()
            # Put the cookies in our return payload so the route can see them
            return {"ok": True, "cookies": cookies_dict}
        try:
            error_data = backend_res.json()
            errores = error_data.get('errors', [])
            mensajes = [e.get('description', e.get('message', 'Error desconocido')) for e in errores]

            if not mensajes:
                mensajes = [f'Error del servidor: HTTP {backend_res.status_code}']

            return {'errores': mensajes}
        except Exception:
            return {'errores': [f'Error del servidor: HTTP {backend_res.status_code}']}
    except requests.exceptions.ConnectionError:
        return {'errores': ['No se pudo conectar con el servidor. Verifica que la API este corriendo.']}


def obtener_perfil(cookies):
    print("cookies:",cookies)
    try:
        response = requests.get(f"{API_BASE_URL}/sesion/perfil", timeout=10,cookies=cookies)
        print("respuesta de backend en obtener perfil:",response,response.status_code,type(response.status_code))
        if response.status_code == 200:
            return response.json()
        try:
            error_data = response.json()
            errores = error_data.get('errors', [])
            mensajes = [e.get('description', e.get('message', 'Error desconocido')) for e in errores]

            if not mensajes:
                mensajes = [f'Error del servidor: HTTP {response.status_code}']

            return {'errores': mensajes}
        except Exception:
            return {'errores': [f'Error del servidor: HTTP {response.status_code}']}
    except requests.exceptions.ConnectionError:
        return {'errores': ['No se pudo conectar con el servidor. Verifica que la API este corriendo.']}
