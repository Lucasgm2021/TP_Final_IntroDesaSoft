import requests

API_BASE_URL = "http://localhost:5000"

def crear_reserva_form_prueba(data):
    data = {}
    try:
        response = requests.post(f"{API_BASE_URL}/reservas/prueba", timeout=10)
        if response:
            data = response.json()
        else:
            print("respuesta no existe, ver.")    
    except Exception as e:
        logger.error(f"Error al crear reserva prueba {padron}: {e}")

    return data