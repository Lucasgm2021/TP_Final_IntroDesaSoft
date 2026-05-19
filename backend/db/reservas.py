import db.config as config

QUERY_GET_RESERVAS = "SELECT reserva_mesa.* FROM reserva_mesa"

QUERY_GET_RESERVA_ID_QR = "SELECT * FROM reserva_mesa WHERE uuid_qr = :uuid_qr"

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
    WHERE fecha = :fecha
    AND hora_reserva = :hora_reserva
    AND estado_reserva IN ('pendiente','confirmada')
) and funcional = true and interior = :interior
"""

QUERY_MESA_DISPONIBLE = """
SELECT id_mesa, capacidad
FROM mesa
WHERE capacidad >= :capacidad and funcional = true and interior = :interior
AND id_mesa NOT IN (
    SELECT id_mesa
    FROM reserva_mesa
    WHERE fecha = :fecha
    AND hora_reserva = :hora_reserva
    AND estado_reserva IN ('pendiente','confirmada')
)
ORDER BY capacidad, id_mesa ASC
LIMIT 1
"""

QUERY_INSERT_RESERVA = """
INSERT INTO reserva
(id_usuario)
VALUES (:id_usuario)
"""

QUERY_INSERT_RESERVA_MESA = """
INSERT INTO reserva_mesa
(id_reserva,id_mesa,interior,fecha,hora_reserva,comensales,uuid_qr,qr_expiracion)
VALUES (:id_reserva,:id_mesa,TRUE,:fecha,:hora_reserva,:comensales,:uuid_qr,:qr_expiracion)
"""

QUERY_GET_RESERVA_ID = "SELECT * FROM reserva_mesa WHERE id_reserva = :id_reserva"

QUERY_UPDATE_ESTADO_QR = """
UPDATE reserva_mesa
SET estado_reserva = :estado_reserva
"""

QUERY_UPDATE_RESERVA = """
UPDATE reserva_mesa
SET """

QUERY_UPDATE_CONTADORES_RESERVA = "UPDATE usuarios"

def obtener_reservas(data,limit=None,offset=None):
    query = QUERY_GET_RESERVAS
    lista_de_condiciones = []
    params = {}
    for key in data:
        lista_de_condiciones.append(f"{key} = :{key}")
        params[key]=data[key]

    if data:
        string_para_query = " and ".join(lista_de_condiciones)
        if "id_usuario" in data:
            query += """ JOIN reserva on reserva_mesa.id_reserva = reserva.id_reserva"""
        query += f" WHERE {string_para_query}"
    if offset is not None and limit is not None:
        paginacion = " LIMIT :limit OFFSET :offset"
        query += " " + paginacion
        params["limit"] = limit
        params["offset"] = offset

    return config.ejecutar_query_lectura(
        query,
        params
    )

def obtener_reserva_por_id(id_reserva):

    resultado = config.ejecutar_query_lectura(
        QUERY_GET_RESERVA_ID,
        params={"id_reserva":id_reserva}
    )

    return resultado[0] if resultado else None

def obtener_reserva_por_qr(uuid_qr):

    resultado = config.ejecutar_query_lectura(
        QUERY_GET_RESERVA_ID_QR,
        params={"uuid_qr":uuid_qr}
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

def obtener_capacidades_mesas_disponibles(fecha, hora, interior):
    resultado = config.ejecutar_query_lectura(
        QUERY_MESAS_DISPONIBLES,
        params={"fecha":fecha,"hora_reserva":hora,"interior":interior}
    )
    resultado = [mesa["capacidad"] for mesa in resultado]
    return resultado

def obtener_mesa_disponible(fecha,hora,comensales,interior):

    resultado = config.ejecutar_query_lectura(
        QUERY_MESA_DISPONIBLE,
        params={"capacidad":comensales,"interior":interior,"fecha":fecha,"hora_reserva":hora}
    )

    return resultado[0] if resultado else None

def obtener_total_mesas_en_uso():
    resultado = config.ejecutar_query_lectura(QUERY_COUNT_MESAS_EN_USO)
    return resultado[0]["total"]

def insertar_reserva(id_usuario):

    return config.ejecutar_query_escritura(
        QUERY_INSERT_RESERVA,
        params={"id_usuario":id_usuario})

def insertar_reserva_mesa(id_reserva,id_mesa,interior,fecha,hora_reserva,comensales,uuid_qr,qr_expiracion):

    return config.ejecutar_query_escritura(
        QUERY_INSERT_RESERVA_MESA,
        params={"id_reserva":id_reserva,"id_mesa":id_mesa,"fecha":fecha,"hora_reserva":hora_reserva,"comensales":comensales,"uuid_qr":uuid_qr,"qr_expiracion":qr_expiracion}
    )

def actualizar_reserva(id_reserva,data):
    query = QUERY_UPDATE_RESERVA
    lista_de_datos_a_modificar = []
    params = {}
    for key in data:
        lista_de_datos_a_modificar.append(f"{key} = :{key}")
        params[key]=data[key]
    string_para_query = ", ".join(lista_de_datos_a_modificar)
    condicion = " WHERE id_reserva = :id_reserva"
    query += string_para_query + condicion
    params["id_reserva"]=id_reserva

    return config.ejecutar_query_escritura(
        query,
        params=params
    )

def actualizar_estado_reserva_por_qr(id_qr_reserva,estado_reserva,estado_qr=None):
    print(id_qr_reserva,estado_reserva,estado_qr)
    params = {}
    params["estado_reserva"]=estado_reserva
    query = QUERY_UPDATE_ESTADO_QR
    if estado_qr:
        query += ", estado_qr = :estado_qr"
        params["estado_qr"]=estado_qr
    query += " WHERE uuid_qr = :uuid_qr"
    params["uuid_qr"]=id_qr_reserva
    return config.ejecutar_query_escritura(
        query,
        params
    )

def actualizar_contadores_reservas_usuario(id_usuario,diferencia_total=None, diferencia_cancelar=None):
    query = QUERY_UPDATE_CONTADORES_RESERVA + " SET"
    params = {}
    valores_a_modificar = []
    if diferencia_total:
        valores_a_modificar.append(" reserva = reserva + :diferencia_total")
        params["diferencia_total"] = diferencia_total

    if diferencia_cancelar:
        valores_a_modificar.append(" canceladas = canceladas + :diferencia_cancelar")
        params["diferencia_cancelar"] = diferencia_cancelar

    query += " and ".join(valores_a_modificar) + " WHERE id_usuario = :id_usuario"
    params["id_usuario"] = id_usuario
    return config.ejecutar_query_escritura(query,params)