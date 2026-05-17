import db.reservas as queries_reservas
import services.mail as servicios_mail
import uuid
from pathlib import Path
from datetime import datetime

ESTADOS_RESERVA = ("pendiente","confirmada","cancelada")

def obtener_reservas(offset,limit,fecha,hora,estado):

    # validar offset y limit
    if not str(offset).isnumeric() or not str(limit).isnumeric():
        raise ValueError("offset y limit deben ser numeros enteros")

    offset = int(offset)
    limit = int(limit)

    if offset < 0 or limit <= 0:
        raise ValueError("offset debe ser >= 0 y limit > 0")

    total_reservas = contar_total_reservas()

    if offset >= total_reservas and total_reservas != 0:
        raise ValueError("offset no puede ser mayor o igual al total de reservas")

    # validar fecha
    if fecha:
        try:
            datetime.strptime(fecha,"%Y-%m-%d")
        except ValueError:
            raise ValueError("Formato de fecha invalido")

    # validar hora
    if hora:
        try:
            datetime.strptime(hora,"%H:%M")
        except ValueError:
            raise ValueError("Formato de hora invalido")

    # validar estado
    if estado and estado not in ESTADOS_RESERVA:
        raise ValueError("Estado invalido")

    reservas = queries_reservas.obtener_reservas(offset,limit,fecha,hora,estado)

    return reservas, total_reservas

def obtener_reservas_por_qr(id_qr):
    return queries_reservas.obtener_reserva_por_qr(id_qr)

def obtener_mesas_disponibles():

    total_mesas = queries_reservas.obtener_total_mesas()
    reservas_activas = queries_reservas.obtener_reservas_activas()

    mesas_disponibles = total_mesas - reservas_activas

    if mesas_disponibles < 0:
        mesas_disponibles = 0

    return mesas_disponibles

def obtener_cantidades_comensales_posibles(fecha, hora):

    try:
        datetime.strptime(fecha,"%Y-%m-%d")
        datetime.strptime(hora,"%H:%M")
    except ValueError:
        raise ValueError("Formato de fecha u hora invalido")

    capacidades = queries_reservas.obtener_capacidades_mesas_disponibles(
        fecha,
        hora
    )

    if not capacidades:
        return []

    capacidad_maxima = max(capacidades)

    return list(range(1, capacidad_maxima + 1))

def contar_total_reservas():
    return list(queries_reservas.obtener_total_reservas()[0].values())[0]

def crear_reserva():

    id_usuario = data.get("id_usuario")
    interior = data.get("interior")
    fecha = data.get("fecha")
    hora = data.get("hora")
    nro_comensales = data.get("nro_comensales")

    if not id_usuario:
        raise ValueError("id_usuario es obligatorio")

    if not fecha or not hora:
        raise ValueError("fecha y hora son obligatorios")

    if not nro_comensales:
        raise ValueError("nro_comensales es obligatorio")

    try:
        datetime.strptime(fecha,"%Y-%m-%d")
        datetime.strptime(hora,"%H:%M")
    except ValueError:
        raise ValueError("Formato de fecha u hora invalido")

    if nro_comensales <= 0:
        raise ValueError("nro_comensales debe ser mayor a 0")

    # buscar mesa disponible
    mesa = queries_reservas.obtener_mesa_disponible(
        fecha,
        hora,
        nro_comensales
    )

    if not mesa:
        raise ValueError("No hay mesas disponibles para esa cantidad de comensales")

    mesa_id = mesa["id"]

    reserva_id = queries_reservas.insertar_reserva(
        id_usuario,
        mesa_id,
        interior,
        fecha,
        hora,
        nro_comensales
    )

    mail_usuario = "lmino@fi.uba.ar"
    mail_template = Path(__file__).resolve().parent / "mail_reserva.html"
    asunto = "RESERVA REGISTRADA"
    datos_mail = {
        "qr_data": "http://localhost:5000/reservas/",
        "url_cancelar": "http://localhost:5000/reservas/cancelar"
    }

    servicios_mail.enviar_mail_con_qr(mail_usuario,asunto,datos_mail,mail_template)
    return reserva_id


def modificar_estado_reserva(data):

    id_reserva = data.get("id_reserva")
    nuevo_estado = data.get("estado")

    if not id_reserva:
        raise ValueError("id_reserva es obligatorio")

    if not nuevo_estado:
        raise ValueError("estado es obligatorio")

    if nuevo_estado not in ESTADOS_RESERVA:
        raise ValueError("Estado invalido")

    reserva = queries_reservas.obtener_reserva_por_id(id_reserva)

    if not reserva:
        raise ValueError("Reserva no encontrada")

    estado_actual = reserva["estado"]

    # regla del sistema
    if estado_actual in ("cancelada"):
        raise ValueError("No se puede modificar una reserva cancelada")

    # regla que definieron
    if estado_actual != "pendiente":
        raise ValueError("Solo se puede modificar una reserva pendiente")

    queries_reservas.actualizar_estado_reserva_mesa(id_reserva,nuevo_estado)

def modificar_estado_reserva_por_qr(id_qr_reserva,estado_reserva,estado_qr):
    queries_reservas.actualizar_estado_reserva_por_qr(id_qr_reserva,estado_reserva,estado_qr)