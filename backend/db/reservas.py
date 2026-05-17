import db.config as config


QUERY_GET_RESERVAS = "SELECT * FROM reserva LIMIT %s OFFSET %s"

QUERY_GET_RESERVA_ID_QR = "SELECT * FROM reserva_mesa WHERE uuid_qr = %s"

QUERY_COUNT_RESERVAS = "SELECT COUNT(*) as total FROM reserva"

QUERY_COUNT_MESAS = " SELECT COUNT(*) as total FROM mesas"

QUERY_MESAS_DISPONIBLES = """
SELECT capacidad
FROM mesas
WHERE id NOT IN (
    SELECT id_mesa
    FROM reserva
    WHERE fecha = %s
    AND hora = %s
    AND estado IN ('pendiente','confirmada')
)
"""

QUERY_MESA_DISPONIBLE = """
SELECT id, capacidad
FROM mesas
WHERE capacidad >= %s
AND id NOT IN (
    SELECT id_mesa
    FROM reserva
    WHERE fecha = %s
    AND hora = %s
    AND estado IN ('pendiente','confirmada')
)
ORDER BY capacidad
LIMIT 1
"""

QUERY_INSERT_RESERVA = """
INSERT INTO reserva
(id_usuario,id_mesa,interior,fecha,hora,nro_comensales,estado)
VALUES (%s,%s,%s,%s,%s,%s,'pendiente')
"""

QUERY_GET_RESERVA_ID = "SELECT * FROM reserva_mesa WHERE id_reserva = %s"


QUERY_UPDATE_ESTADO = """
UPDATE reserva
SET estado = %s
WHERE id = %s
"""

QUERY_UPDATE_ESTADO_QR = """
UPDATE reserva
SET estado_qr = %s
WHERE uuid_qr = %s
"""

QUERY_UPDATE_ESTADO_RESERVA = """
UPDATE reserva_mesa
SET estado = %s
WHERE id_reserva = %s
"""

def obtener_reservas(offset, limit):
    return config.ejecutar_query_lectura(
        QUERY_GET_RESERVAS,
        params=(limit, offset)
    )

def obtener_reserva_por_id(id_reserva):

    resultado = config.ejecutar_query_lectura(
        QUERY_GET_RESERVA_ID,
        params=(id_reserva,)
    )

    return resultado[0] if resultado else None

def obtener_reserva_por_qr(id_reserva_qr):

    resultado = config.ejecutar_query_lectura(
        QUERY_GET_RESERVA_ID_QR,
        params=(id_reserva_qr,)
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