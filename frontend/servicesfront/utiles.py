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
        
    