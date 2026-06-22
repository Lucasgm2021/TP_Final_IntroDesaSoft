import db.config as config

QUERY_GET_RESERVAS = """
SELECT
    reserva.*,
    reserva_mesa.id_mesa
FROM reserva
LEFT JOIN reserva_mesa
    ON reserva.id_reserva = reserva_mesa.id_reserva
"""

QUERY_GET_RESERVAS_SIN_MESAS = """
    SELECT * FROM reserva
"""

QUERY_GET_RESERVA_ID_QR = """
SELECT
    reserva.*,
    reserva_mesa.id_mesa
FROM reserva
LEFT JOIN reserva_mesa
    ON reserva.id_reserva = reserva_mesa.id_reserva
WHERE reserva.uuid_qr = :uuid_qr
"""

QUERY_COUNT_RESERVAS = "SELECT COUNT(*) as total FROM reserva"

QUERY_INSERT_RESERVA = """
INSERT INTO reserva (
    id_usuario,
    estado_reserva,
    hora_reserva,
    fecha,
    interior,
    uuid_qr,
    qr_expiracion,
    comensales
)
VALUES (
    :id_usuario,
    'pendiente',
    :hora_reserva,
    :fecha,
    :interior,
    :uuid_qr,
    :qr_expiracion,
    :comensales
)
"""

QUERY_INSERT_RESERVA_MESA = """
INSERT INTO reserva_mesa
(id_reserva,id_mesa)
VALUES (:id_reserva,:id_mesa)
"""

QUERY_GET_RESERVA_MESA_ID = "SELECT * FROM reserva_mesa WHERE id_reserva = :id_reserva"

QUERY_GET_RESERVA_ID = "SELECT * FROM reserva WHERE id_reserva = :id_reserva"

QUERY_UPDATE_ESTADO_QR = """
UPDATE reserva
SET estado_reserva = :estado_reserva
"""

QUERY_UPDATE_RESERVA = """
UPDATE reserva
SET
"""

QUERY_UPDATE_CONTADORES_RESERVA = "UPDATE usuarios"

def obtener_reservas(data):
    query = ""
    if data["mesas"]:
        query = QUERY_GET_RESERVAS
    else:
        query = QUERY_GET_RESERVAS_SIN_MESAS

    #borro la clave y valor de mesas ya que no es una condicion para el where.
    del data["mesas"]
    
    lista_de_condiciones = []
    params = {}
    for key in data:
        lista_de_condiciones.append(f"reserva.{key} = :{key}")
        params[key]=data[key]

    if data:
        string_para_query = " and ".join(lista_de_condiciones)
        query += f" WHERE {string_para_query}"

    return config.ejecutar_query_lectura(
        query,
        params
    )

def obtener_reserva_mesa_por_id(id_reserva):

    resultado = config.ejecutar_query_lectura(
        QUERY_GET_RESERVA_MESA_ID,
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

def obtener_reserva_por_id(id_reserva):
    resultado = config.ejecutar_query_lectura(QUERY_GET_RESERVA_ID,{"id_reserva":id_reserva})
    return resultado[0] if resultado else None

def insertar_reserva(interior,id_usuario,fecha,hora_reserva,comensales,uuid_qr,qr_expiracion):
    return config.ejecutar_query_escritura(
        QUERY_INSERT_RESERVA,
        params={"interior":interior,"id_usuario":id_usuario,"fecha":fecha,"hora_reserva":hora_reserva,"comensales":comensales,"uuid_qr":uuid_qr,"qr_expiracion":qr_expiracion})

def insertar_reserva_mesa(id_reserva,id_mesa):

    return config.ejecutar_query_escritura(
        QUERY_INSERT_RESERVA_MESA,
        params={"id_reserva":id_reserva,"id_mesa":id_mesa}
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
        valores_a_modificar.append(" reservas = reservas + :diferencia_total")
        params["diferencia_total"] = diferencia_total

    if diferencia_cancelar:
        valores_a_modificar.append(" canceladas = canceladas + :diferencia_cancelar")
        params["diferencia_cancelar"] = diferencia_cancelar

    query += ", ".join(valores_a_modificar) + " WHERE id_usuario = :id_usuario"
    params["id_usuario"] = id_usuario
    return config.ejecutar_query_escritura(query,params)