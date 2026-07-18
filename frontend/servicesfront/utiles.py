import requests
from constants import TIMEOUT_REQUEST,HTTP_CODE_OK

def leer_respuesta_request(response,code, json=False):
    try:
        if response.status_code == code:
            if json:
                return response.json()
            else:
                return {'ok': True}
        else:                     
            error_data = response.json()
            errores = error_data.get('errors', [])
            mensajes = [e.get('description') if len(e.get('description', '')) > 0 else e.get('message', 'Error desconocido') for e in errores]

            if not mensajes:
                mensajes = [f'Error del servidor: HTTP {response.status_code}']

            return {'errores': mensajes}
    except:
        return {'errores': [f'Error del servidor al leer json de respuesta: HTTP {response.status_code}']} 
        
def request_backend(method, endpoint, *, params=None, json_data=None, data=None, files=None, cookies=None, expected_status=HTTP_CODE_OK, return_json=False, timeout=TIMEOUT_REQUEST):
    try:
        response = requests.request(
        method=method.upper(),
        url=endpoint,
        params=params,
        json=json_data,
        data=data,
        files=files,
        cookies=cookies,
        timeout=timeout,
        )
        return leer_respuesta_request(response, expected_status, json=return_json)
    except requests.exceptions.ConnectionError:
        return {"errores": ["No se pudo conectar con el servidor."]}
    except requests.RequestException:
        return {"errores": ["Ocurrió un error inesperado al realizar la petición. Inténtalo de nuevo más tarde."]}    