import db.config as config

QUERY_GET_RESERVAS = "SELECT * FROM reserva_mesa"

QUERY_GET_RESERVA_ID_QR = "SELECT * FROM reserva_mesa WHERE uuid_qr = %s"

QUERY_COUNT_RESERVAS = "SELECT COUNT(*) as total FROM reserva"

QUERY_COUNT_MESAS = " SELECT COUNT(*) as total FROM mesa"

QUERY_COUNT_MESAS_EN_USO = """SELECT COUNT(*) as total FROM reserva_mesa
WHERE fecha = DATE(NOW()) and hora_reserva = CONCAT(HOUR(NOW()), ':00:00') and estado_reserva = 'finalizada'
"""

QUERY_MESAS_DISPONIBLES = """
SELECT capacidad
FROM mesa
WHERE id_mesa NOT IN (
    SELECT id_mesa
    FROM reserva_mesa
    WHERE fecha = %s
    AND hora_reserva = %s
    AND estado_reserva IN ('pendiente','confirmada')
)
"""

QUERY_MESA_DISPONIBLE = """
SELECT id_mesa, capacidad
FROM mesa
WHERE capacidad >= %s
AND id_mesa NOT IN (
    SELECT id_mesa
    FROM reserva_mesa
    WHERE fecha = %s
    AND hora_reserva = %s
    AND estado_reserva IN ('pendiente','confirmada')
)
ORDER BY capacidad, id_mesa ASC
LIMIT 1
"""

QUERY_INSERT_RESERVA = """
INSERT INTO reserva
(id_usuario)
VALUES (%s)
"""

QUERY_INSERT_RESERVA_MESA = """
INSERT INTO reserva_mesa
(id_reserva,id_mesa,interior,fecha,hora_reserva,comensales,uuid_qr,qr_expiracion)
VALUES (%s,%s,TRUE,%s,%s,%s,%s,%s)
"""

QUERY_GET_RESERVA_ID = "SELECT * FROM reserva_mesa WHERE id_reserva = %s"

QUERY_UPDATE_ESTADO_QR = """
UPDATE reserva_mesa
SET estado_reserva = %s
"""

QUERY_UPDATE_RESERVA = """
UPDATE reserva_mesa
SET """

def obtener_reservas(data,limit=None,offset=None):
    query = QUERY_GET_RESERVAS
    lista_de_condiciones = []
    valores_de_condicion = []
    for key in data:
        lista_de_condiciones.append(f"{key} = %s")
        valores_de_condicion.append(data[key])

    if data:
        string_para_query = " and ".join(lista_de_condiciones)
        query += f" WHERE {string_para_query}"
    lista_params = valores_de_condicion
    if offset and limit:
        paginacion = " LIMIT %s OFFSET %s"
        query += " " + paginacion
        lista_params += [limit,offset]
    tupla_params = tuple(lista_params)

    return config.ejecutar_query_lectura(
        query,
        params=tupla_params
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
    print("query: ",QUERY_MESAS_DISPONIBLES % (fecha,hora))
    resultado = config.ejecutar_query_lectura(
        QUERY_MESAS_DISPONIBLES,
        params=(fecha,hora)
    )
    print(resultado)
    resultado = [mesa["capacidad"] for mesa in resultado]
    print(resultado)
    return resultado

def obtener_mesa_disponible(fecha,hora,comensales):

    resultado = config.ejecutar_query_lectura(
        QUERY_MESA_DISPONIBLE,
        params=(comensales,fecha,hora)
    )

    return resultado[0] if resultado else None

def insertar_reserva(id_usuario):

    return config.ejecutar_query_escritura(
        QUERY_INSERT_RESERVA,
        params=(id_usuario,)
    )

def insertar_reserva_mesa(id_reserva,id_mesa,interior,fecha,hora_reserva,comensales,uuid_qr,qr_expiracion):

    return config.ejecutar_query_escritura(
        QUERY_INSERT_RESERVA_MESA,
        params=(id_reserva,id_mesa,fecha,hora_reserva,comensales,uuid_qr,qr_expiracion)
    )

def actualizar_reserva(id_reserva,data):
    query = QUERY_UPDATE_RESERVA
    lista_de_datos_a_modificar = []
    valores_a_modificar = []
    for key in data:
        lista_de_datos_a_modificar.append(f"{key} = %s")
        valores_a_modificar.append(data[key])
    string_para_query = ", ".join(lista_de_datos_a_modificar)
    condicion = " WHERE id_reserva = %s"
    query += string_para_query + condicion
    params = tuple(valores_a_modificar + [id_reserva])
    print(query)
    return config.ejecutar_query_escritura(
        query,
        params=params
    )

def actualizar_estado_reserva_por_qr(id_qr_reserva,estado_reserva,estado_qr=None):
    params = [estado_reserva]
    query = QUERY_UPDATE_ESTADO_QR
    if estado_qr:
        query += ", estado_qr = %s"
        params = params + [estado_qr]
    query += " WHERE uuid_qr = %s"
    params = params + [id_qr_reserva]
    print(query, params)
    params = tuple(params)
    return config.ejecutar_query_escritura(
        query,
        params=params
    )

def obtener_total_mesas_en_uso():
    resultado = config.ejecutar_query_lectura(QUERY_COUNT_MESAS_EN_USO)
    return resultado[0]["total"]