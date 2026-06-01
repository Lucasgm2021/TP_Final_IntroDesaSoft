import requests
from constants import API_BASE_URL

def crear_reserva(hora_reserva,dia_reserva,nro_comensales,interior,ids_mesas,cookies):
    data = {}
    try:
        response = requests.post(f"{API_BASE_URL}/reservas",json={
            "hora": hora_reserva,
            "fecha": dia_reserva,
            "nro_comensales": nro_comensales,
            "interior": interior,
            "ids_mesas": ids_mesas
        }, timeout=10,cookies=cookies)
        if response.status_code == 201:
            return {"ok":True}
        try:
            error_data = response.json()
            errores = error_data.get('errors', [])
            mensajes = [e.get('description', 'Error desconocido') for e in errores]
            if not mensajes:
                mensajes = [f'Error del servidor: HTTP {response.status_code}']

            return {'errores': mensajes,"code":response.status_code}
        except Exception:
            return {'errores': [f'Error del servidor: HTTP {response.status_code}']}
    except requests.exceptions.ConnectionError:
        return {'errores': ['No se pudo conectar con el servidor. Verifica que la API este corriendo.']}

    return data

def obtener_mesas(fecha,hora,ubicacion_bool,comensales,cookies):
    try:
        response = requests.get(f"{API_BASE_URL}/mesas/validacion", params={
            "fecha": fecha,
            "hora": hora,
            "interior": ubicacion_bool
        }, timeout=10,cookies=cookies)
        if response.status_code == 200:
            return response.json()
        else:
            error_data = response.json()
            errores = error_data.get('errors', [])
            mensajes = [e.get('description', e.get('message', 'Error desconocido')) for e in errores]

            if not mensajes:
                mensajes = [f'Error del servidor: HTTP {response.status_code}']

            return {'errores': mensajes,"code":response.status_code}
    except requests.exceptions.ConnectionError:
        return {'errores': ['No se pudo conectar con el servidor. Verifica que la API este corriendo.']}

def obtener_mis_reservas(cookies):
    try:
        response = requests.get(f"{API_BASE_URL}/reservas", timeout=10, cookies=cookies)
        if response.status_code == 200:
            return response.json()
        else:
            error_data = response.json()
            errores = error_data.get('errors', [])
            mensajes = [e.get('description', e.get('message', 'Error desconocido')) for e in errores]
            if not mensajes:
                mensajes = [f'Error del servidor: HTTP {response.status_code}']

            return {'errores': mensajes,"code":response.status_code}
    except requests.exceptions.ConnectionError:
        return {'errores': ['No se pudo conectar con el servidor. Verifica que la API este corriendo.']}

def cancelar_reserva(uuid_reserva,cookies):
    try:
        response = requests.post(f"{API_BASE_URL}/reservas/cancelar/{uuid_reserva}", timeout=10, cookies=cookies)
        if response.status_code == 201:
            return {"ok": True}
        else:
            error_data = response.json()
            errores = error_data.get('errors', [])
            mensajes = [e.get('description', e.get('message', 'Error desconocido')) for e in errores]

            if not mensajes:
                mensajes = [f'Error del servidor: HTTP {response.status_code}']

            return {'errores': mensajes,"code":response.status_code}
    except requests.exceptions.ConnectionError:
        return {'errores': ['No se pudo conectar con el servidor. Verifica que la API este corriendo.']}

def obtener_reservas_admin(limit,estado_reserva,cookies):
    try:
        params = {'_limit': limit}
        if estado_reserva:
            params['estado'] = estado_reserva
        response = requests.get(f"{API_BASE_URL}/reservas", params=params, timeout=10, cookies=cookies)
        if response.status_code == 200:
            data = response.json()

            return response.json()
        else:
            error_data = response.json()
            errores = error_data.get('errors', [])
            mensajes = [e.get('description', e.get('message', 'Error desconocido')) for e in errores]
            if not mensajes:
                mensajes = [f'Error del servidor: HTTP {response.status_code}']

            return {'errores': mensajes,"code":response.status_code}
    except requests.exceptions.ConnectionError:
        return {'errores': ['No se pudo conectar con el servidor. Verifica que la API este corriendo.']}