import requests
from constants import API_BASE_URL
from servicesfront.utiles import leer_respuesta_request

def crear_reseña(id_reserva,calificacion,comentario,cookies):
    try:
        response = requests.post(f"{API_BASE_URL}/reseñas",json={
            "id_reserva": id_reserva,
            "calificacion": calificacion,
            "comentario": comentario
        }, timeout=10,cookies=cookies)
        return leer_respuesta_request(response,201)
    except requests.exceptions.ConnectionError:
        return {'errores': ['No se pudo conectar con el servidor.']}
    except:
        return {'errores': ['Ocurrió un error inesperado al crear la reserva. Inténtalo de nuevo más tarde.']}