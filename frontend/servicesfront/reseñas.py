import requests
from constants import API_BASE_URL

def crear_reseña(id_reserva,calificacion,comentario,cookies):
    try:
        response = requests.post(f"{API_BASE_URL}/reseñas",json={
            "id_reserva": id_reserva,
            "calificacion": calificacion,
            "comentario": comentario
        }, timeout=10,cookies=cookies)

        if response.status_code == 201:
            return {"ok":True}

        error_data = response.json()
        errores = error_data.get('errors', [])
        mensajes = [e.get('description') if len(e.get('description', '')) > 0 else e.get('message', 'Error desconocido') for e in errores]
        if not mensajes:
            mensajes = [f'Error del servidor: HTTP {response.status_code}']

        return {'errores': mensajes,"code":response.status_code}

    except requests.exceptions.ConnectionError:
        return {'errores': ['No se pudo conectar con el servidor.']}
    except:
        return {'errores': ['Ocurrió un error inesperado al crear la reserva. Inténtalo de nuevo más tarde.']}
    return data