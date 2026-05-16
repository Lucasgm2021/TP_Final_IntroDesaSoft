import db.config as config


QUERY_GET_RESERVAS = "SELECT * FROM reserva LIMIT %s OFFSET %s"

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

QUERY_GET_RESERVA_ID = "SELECT * FROM reserva WHERE id = %s"

QUERY_UPDATE_ESTADO = """
UPDATE reserva
SET estado = %s
WHERE id = %s
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

def obtener_total_reservas():

    resultado = config.ejecutar_query_lectura(
        QUERY_COUNT_RESERVAS
    )

    return resultado[0]["total"]

def obtener_total_mesas():

    resultado = config.ejecutar_query_lectura(
        QUERY_COUNT_MESAS
    )

    return resultado[0]["total"]

def obtener_capacidades_mesas_disponibles(fecha, hora):

    resultado = config.ejecutar_query_lectura(
        QUERY_MESAS_DISPONIBLES,
        params=(fecha,hora)
    )

    return [r["capacidad"] for r in resultado]

def obtener_mesa_disponible(fecha,hora,comensales):

    resultado = config.ejecutar_query_lectura(
        QUERY_MESA_DISPONIBLE,
        params=(comensales,fecha,hora)
    )

    return resultado[0] if resultado else None

def insertar_reserva(id_usuario,mesa_id,interior,fecha,hora,comensales):

    return config.ejecutar_query_escritura(
        QUERY_INSERT_RESERVA,
        params=(id_usuario,mesa_id,interior,fecha,hora,comensales)
    )

def actualizar_estado_reserva(id_reserva,estado):

    return config.ejecutar_query_escritura(
        QUERY_UPDATE_ESTADO,
        params=(estado,id_reserva)
    )