import db.config as config

QUERY_GET_RESERVAS = "SELECT * FROM reserva LIMIT %s OFFSET %s"
QUERY_COUNT_RESERVAS = """SELECT TABLE_ROWS FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'restaurante' AND TABLE_NAME = 'reserva';"""

def obtener_reservas(offset,limit):
    return config.ejecutar_query_lectura(QUERY_GET_RESERVAS,params=(limit,offset))

def obtener_total_reservas():
    return config.ejecutar_query_lectura(QUERY_COUNT_RESERVAS)