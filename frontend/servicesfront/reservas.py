import requests
from constants import API_BASE_URL
from servicesfront.utiles import leer_respuesta_request

def crear_reserva(hora_reserva,dia_reserva,nro_comensales,interior,ids_mesas,cookies):
    try:
        response = requests.post(f"{API_BASE_URL}/reservas",json={
            "hora": hora_reserva,
            "fecha": dia_reserva,
            "nro_comensales": nro_comensales,
            "interior": interior,
            "ids_mesas": ids_mesas
        }, timeout=10,cookies=cookies)
        return leer_respuesta_request(response,201)
    except requests.exceptions.ConnectionError:
        return {'errores': ['No se pudo conectar con el servidor.']}
    except:
        return {'errores': ['Ocurrió un error inesperado al crear la reserva. Inténtalo de nuevo más tarde.']}

def obtener_mesas(fecha,hora,ubicacion_bool,comensales,cookies):
    try:
        response = requests.get(f"{API_BASE_URL}/mesas/validacion", params={
            "fecha": fecha,
            "hora": hora,
            "interior": ubicacion_bool
        }, timeout=10,cookies=cookies)
        return leer_respuesta_request(response,200,json=True)
    except requests.exceptions.ConnectionError:
        return {'errores': ['No se pudo conectar con el servidor.']}
    except:
        return {'errores': ['Ocurrió un error inesperado al obtener las mesas. Inténtalo de nuevo más tarde.']}

def obtener_mis_reservas(id_usuario,cookies):
    try:
        response = requests.get(f"{API_BASE_URL}/reservas", params={"id_usuario":id_usuario,"mesas":"false"},timeout=10, cookies=cookies)
        return leer_respuesta_request(response,200,json=True)
    except requests.exceptions.ConnectionError:
        return {'errores': ['No se pudo conectar con el servidor.']}
    except:
        return {'errores': ['Ocurrió un error inesperado al obtener las reservas. Inténtalo de nuevo más tarde.']}

def cancelar_reserva(uuid_reserva,cookies):
    try:
        response = requests.patch(f"{API_BASE_URL}/reservas/cancelar/{uuid_reserva}", timeout=10, cookies=cookies)
        return leer_respuesta_request(response,201)
    except requests.exceptions.ConnectionError:
        return {'errores': ['No se pudo conectar con el servidor.']}
    except:
        return {'errores': ['Ocurrió un error inesperado al cancelar la reserva. Inténtalo de nuevo más tarde.']}

def confirmar_reserva(uuid_reserva,cookies):
    try:
        response = requests.patch(f"{API_BASE_URL}/reservas/confirmar/{uuid_reserva}", timeout=10, cookies=cookies)
        return leer_respuesta_request(response,201)
    except requests.exceptions.ConnectionError:
        return {'errores': ['No se pudo conectar con el servidor.']}
    except:
        return {'errores': ['Ocurrió un error inesperado al cancelar la reserva. Inténtalo de nuevo más tarde.']}

def obtener_reservas_admin(limit,cookies,estado_reserva=None):
    try:
        params = {'_limit': limit}
        if estado_reserva:
            params['estado'] = estado_reserva
        response = requests.get(f"{API_BASE_URL}/reservas", params=params, timeout=10, cookies=cookies)
        return leer_respuesta_request(response,200,json=True)
    except requests.exceptions.ConnectionError:
        return {'errores': ['No se pudo conectar con el servidor.']}
    except:
        return {'errores': ['Ocurrió un error inesperado al obtener las reservas. Inténtalo de nuevo más tarde.']}

def obtener_mis_reseñas(cookies):
    try:
        response = requests.get(f"{API_BASE_URL}/reseñas/usuario", timeout=10, cookies=cookies)
        return leer_respuesta_request(response,200,json=True)
    except requests.exceptions.ConnectionError:
        return {'errores': ['No se pudo conectar con el servidor.']}
    except:
        return {'errores': ['Ocurrió un error inesperado al obtener las reservas. Inténtalo de nuevo más tarde.']}
