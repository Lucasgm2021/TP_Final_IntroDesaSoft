from constants import API_BASE_URL,HTTP_CODE_OK,HTTP_CODE_CREATED,HTTP_GET,HTTP_POST,HTTP_PATCH
from servicesfront.utiles import leer_respuesta_request, request_backend

def crear_reserva(hora_reserva,dia_reserva,nro_comensales,interior,ids_mesas,cookies):
    return request_backend(HTTP_POST, f"{API_BASE_URL}/reservas", json_data={
        "hora": hora_reserva,
        "fecha": dia_reserva,
        "nro_comensales": nro_comensales,
        "interior": interior,
        "ids_mesas": ids_mesas
    }, cookies=cookies, expected_status=HTTP_CODE_CREATED)


def obtener_mesas(fecha,hora,ubicacion_bool,comensales,cookies):
    return request_backend(HTTP_GET,f"{API_BASE_URL}/mesas/validacion",params={
            "fecha": fecha,
            "hora": hora,
            "interior": ubicacion_bool
        }, cookies=cookies, expected_status=HTTP_CODE_OK,return_json=True)

def obtener_mis_reservas(id_usuario,cookies):
    return request_backend(HTTP_GET,f"{API_BASE_URL}/reservas",params={
        "id_usuario": id_usuario,
        "mesas": "false"
    }, cookies=cookies, expected_status=HTTP_CODE_OK,return_json=True)

def cancelar_reserva(uuid_reserva,cookies):
    return request_backend(HTTP_PATCH,f"{API_BASE_URL}/reservas/cancelar/{uuid_reserva}", cookies=cookies, expected_status=HTTP_CODE_CREATED)

def confirmar_reserva(uuid_reserva,cookies):
    return request_backend(HTTP_PATCH,f"{API_BASE_URL}/reservas/confirmar/{uuid_reserva}", cookies=cookies, expected_status=HTTP_CODE_CREATED)

def obtener_reservas_admin(limit,cookies,estado_reserva=None):
    params = {'_limit': limit}
    if estado_reserva:
        params['estado'] = estado_reserva
    return request_backend(HTTP_GET,f"{API_BASE_URL}/reservas", params=params, cookies=cookies, expected_status=HTTP_CODE_OK, return_json=True)

def obtener_mis_reseñas(cookies):
    return request_backend(HTTP_GET,f"{API_BASE_URL}/reseñas/usuario", cookies=cookies, expected_status=HTTP_CODE_OK, return_json=True)
