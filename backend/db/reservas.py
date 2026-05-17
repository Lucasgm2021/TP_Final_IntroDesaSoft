import db.config as config

QUERY_GET_RESERVAS = "SELECT * FROM reserva WHERE uuid_qr = %s"
QUERY_COUNT_RESERVAS = """SELECT TABLE_ROWS FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'restaurante' AND TABLE_NAME = 'reserva';"""

QUERY_GET_RESERVA_ID = "SELECT * FROM reserva_mesa WHERE id_reserva = %s"

QUERY_UPDATE_ESTADO_RESERVA = """
UPDATE reserva_mesa
SET estado = %s
WHERE id_reserva = %s
"""

QUERY_UPDATE_ESTADO_QR = """
UPDATE reserva
SET estado_qr = %s
WHERE uuid_qr = %s
"""

def obtener_reservas(id_hash):
    return config.ejecutar_query_lectura(
        QUERY_GET_RESERVAS,params=(id_hash,)
    )

def obtener_reserva_por_id(id_reserva):

    resultado = config.ejecutar_query_lectura(
        QUERY_GET_RESERVA_ID,
        params=(id_reserva,)
    )

    return resultado[0] if resultado else None

def obtener_total_reservas():
    return config.ejecutar_query_lectura(QUERY_COUNT_RESERVAS)

def actualizar_estado_reserva_qr(data):
    data = tuple([data["estado_qr"],data["uuid_qr"]])
    print("data para query estado reserva:",data,type(data))
    return config.ejecutar_query_escritura(
        QUERY_UPDATE_ESTADO_QR,
        params=data
    )

def actualizar_estado_reserva_mesa(id_reserva,estado):

    return config.ejecutar_query_escritura(
        QUERY_UPDATE_ESTADO_RESERVA,
        params=(estado,id_reserva)
    )