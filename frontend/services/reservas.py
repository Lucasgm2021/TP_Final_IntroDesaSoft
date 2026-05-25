import requests

API_BASE_URL = "http://localhost:5000"

def crear_reserva_form_prueba(hora_reserva,dia_reserva,nro_comensales,interior,cookies):
    data = {}
    try:
        response = requests.post(f"{API_BASE_URL}/reservas",json={
            "hora": hora_reserva,
            "fecha": dia_reserva,
            "nro_comensales": nro_comensales,
            "interior": interior
        }, timeout=10,cookies=cookies)
        print("respuesta de backend:",response,response.status_code,type(response.status_code))
        if response.status_code == 201:
            return {"ok":True}
        try:
            error_data = response.json()
            print("data de error del backend:",error_data)
            errores = error_data.get('errors', [])
            mensajes = [e.get('description', e.get('message', 'Error desconocido')) for e in errores]

            if not mensajes:
                mensajes = [f'Error del servidor: HTTP {response.status_code}']

            return {'errores': mensajes,"code":response.status_code}
        except Exception:
            return {'errores': [f'Error del servidor: HTTP {response.status_code}']}
    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")

        return {'errores': ['No se pudo conectar con el servidor. Verifica que la API este corriendo.']}


    return data