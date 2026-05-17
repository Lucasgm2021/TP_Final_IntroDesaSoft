import db.reservas as queries_reservas
import services.mail as servicios_mail
import uuid
from pathlib import Path

ESTADOS_RESERVA = ("pendiente","cancelada","finalizada")

def obtener_reservas(offset,limit,fecha,hora,estado,id_hash):

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

    reservas = queries_reservas.obtener_reservas(id_hash)

    return reservas, total_reservas

def contar_total_reservas():
    return list(queries_reservas.obtener_total_reservas()[0].values())[0]

def crear_reserva():

    mail_usuario = "lmino@fi.uba.ar"
    mail_template = Path(__file__).resolve().parent / "mail_reserva.html"
    asunto = "RESERVA REGISTRADA"
    datos_mail = {
        "qr_data": "http://localhost:5000/reservas/",
        "url_cancelar": "http://localhost:5000/reservas/cancelar"
    }

    servicios_mail.enviar_mail_con_qr(mail_usuario,asunto,datos_mail,mail_template)
    return "Todo ok",200

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
    print(reserva)
    estado_actual = reserva["estado"]

    # regla del sistema
    if estado_actual in ("cancelada"):
        raise ValueError("No se puede modificar una reserva cancelada")

    # regla que definieron
    if estado_actual != "pendiente":
        raise ValueError("Solo se puede modificar una reserva pendiente")

    queries_reservas.actualizar_estado_reserva_mesa(id_reserva,nuevo_estado)

def modificar_estado_qr(data):
    queries_reservas.actualizar_estado_reserva_qr(data)