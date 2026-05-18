import uuid
from pathlib import Path
from datetime import datetime,timedelta
import db.reservas as queries_reservas
import services.mail as servicios_mail
from services.messages import error_msg, paginacion_msg

ESTADOS_RESERVA = ("pendiente","confirmada","cancelada")

def obtener_reservas(offset,limit,fecha,hora,estado):
    # validar offset y limit
    if not str(offset).isnumeric() or not str(limit).isnumeric():
        return error_msg(400,"Parametros invalidos",description="offset y limit deben ser numeros enteros")
    offset = int(offset)
    limit = int(limit)

    if offset < 0 or limit <= 0:
        return error_msg(400,"Parametros invalidos",description="offset debe ser 0 o mayor y limit debe ser mayor a 0")

    total_reservas = contar_total_reservas()
    if offset >= total_reservas and total_reservas != 0:
        return error_msg(400,"Parametros invalidos",description="offset no puede ser mayor o igual al total de usuarios")

    # validar fecha
    if fecha:
        try:
            datetime.strptime(fecha,"%Y-%m-%d")
        except ValueError:
            return error_msg(400,"Parametros invalidos",description="Fecha debe tener formato YYY-mm-dd")

    # validar hora
    if hora:
        try:
            datetime.strptime(hora,"%H:%M")
        except ValueError:
            return error_msg(400,"Parametros invalidos",description="Hora debe tener formato HH:MM")

    # validar estado
    if estado and estado not in ESTADOS_RESERVA:
           return error_msg(400,"Parametros invalidos",description="Estado no valido")
    try:
        reservas = queries_reservas.obtener_reservas(offset,limit)
        #fecha es datetime.date, hora es datetime.timedelta y qr_expiracion es datetime.datetime
        reservas = [{**reserva, "fecha": reserva["fecha"].strftime('%Y-%m-%d'),"hora_reserva": str(reserva["hora_reserva"]), "qr_expiracion": str(reserva["qr_expiracion"])}  for reserva in reservas]
    except:
        return error_msg(500,"Error obteniendo reservas",description="Ha ocurrido un error en el servidor.")

    return paginacion_msg(
        reservas,
        limit,
        offset,
        total_reservas,
        "http://localhost:5000/reservas",
        "reservas",
        200
    )
    

    return reservas, total_reservas

def obtener_mesas_disponibles():
    #total de mesas - mesas usadas en un determinado momento = mesas disponibles en ese momento
    total_mesas = queries_reservas.obtener_total_mesas()
    mesas_en_uso = queries_reservas.obtener_total_mesas_en_uso()

    mesas_disponibles = total_mesas - mesas_en_uso

    if mesas_disponibles < 0:
        mesas_disponibles = 0

    return {"mesas_disponibles":mesas_disponibles},200

def obtener_cantidades_comensales_posibles(fecha, hora):
    if not fecha or not hora:
        return error_msg(400,"Parametros invalidos","fecha y hora son obligatorios")
    try:
        datetime.strptime(fecha,"%Y-%m-%d")
        datetime.strptime(hora,"%H:%M:%S")
    except ValueError:
        return error_msg(400,"Parametros invalidos",description="Fecha u hora con formato incorrecto.")

    try: 
        capacidades = queries_reservas.obtener_capacidades_mesas_disponibles(
            fecha,
            hora
        )
    except:
        return error_msg(500,"Error obteniendo reservas",description="Ha ocurrido un error en el servidor.")

    if not capacidades:
        return jsonify({"Msg":"No hay mesas disponibles en esa fecha y hora."}),200

    capacidad_maxima = max(capacidades)
    return {"Listado de capacidades disponibles": list(range(1, capacidad_maxima + 1))},200

def contar_total_reservas():
    return queries_reservas.obtener_total_reservas()

def crear_reserva(data):
    if not data:
        return error_msg(400,"Body invalido","Debe enviarse JSON")
    id_usuario = data.get("id_usuario")
    interior = data.get("interior")
    fecha = data.get("fecha")
    hora = data.get("hora")
    nro_comensales = data.get("nro_comensales")

    if not id_usuario:
        return error_msg(400,"Parametros invalidos","id_usuario es obligatorio")

    if not fecha or not hora:
        return error_msg(400,"Parametros invalidos","fecha y hora son obligatorios")

    if not nro_comensales:
        return error_msg(400,"Parametros invalidos","nro_comensales es obligatorio")

    if interior is None:
        return error_msg(400,"Parametros invalidos","interior es obligatorio")

    try:
        datetime.strptime(fecha,"%Y-%m-%d")
        datetime.strptime(hora,"%H:%M:%S")
        time_stamp = fecha + " " + hora
        fecha_hora = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return error_msg(400,"Parametros invalidos",description="Fecha u hora con formato incorrecto.")

    if nro_comensales <= 0:
        return error_msg(400,"Parametros invalidos","nro_comensales debe ser mayor a 0")

    if not isinstance(interior, bool):
        return error_msg(400,"Parametros invalidos","interior debe ser un booleano")

    if fecha_hora <= datetime.now():
        return error_msg(400,"Parametros invalidos","La fecha y hora ingresadas no pueden ser anteriores al instante actual.")       

    # buscar mesa disponible
    mesa = queries_reservas.obtener_mesa_disponible(
        fecha,
        hora,
        nro_comensales
    )

    if not mesa:
        raise ValueError("No hay mesas disponibles para esa cantidad de comensales")
    print("mesa: ",mesa)
    id_mesa = mesa["id_mesa"]
    try:
        reserva_id = queries_reservas.insertar_reserva(
            id_usuario,
        )

        fecha_hora_mas_30min = fecha_hora + timedelta(minutes=30)
        uuid_qr = str(uuid.uuid4()).replace("-","")

        queries_reservas.insertar_reserva_mesa(
            reserva_id,
            id_mesa,interior,fecha,hora,nro_comensales,uuid_qr,qr_expiracion=fecha_hora_mas_30min
        )
    
        mail_usuario = "lmino@fi.uba.ar"
        mail_template = Path(__file__).resolve().parent / "mail_reserva.html"
        asunto = "RESERVA REGISTRADA"
        datos_mail = {
            "qr_data": f"http://localhost:5000/reservas/mostrar_confirmacion?code={uuid_qr}",
            "url_cancelar": f"http://localhost:5000/reservas/mostrar_cancelacion?code={uuid_qr}"
        }

        servicios_mail.enviar_mail_con_qr(mail_usuario,asunto,datos_mail,mail_template)
    except:
        return error_msg(500,"Error obteniendo reservas",description="Ha ocurrido un error en el servidor.")
    return {"msg":"Reserva creada exitosamente","id": reserva_id},201


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

def confirmar_reserva_por_qr(id_qr_reserva):
    res  = queries_reservas.obtener_reserva_por_qr(id_qr_reserva)
    if not res:
        return error_msg(404,"Error: reserva no encontrada",description="No existe una reserva con ese ID.")

    if res["estado_qr"] != "pendiente":
        return error_msg(400,"Error: Reserva no valida.",description="El QR ya fue leido o expiró.")


    if res["qr_expiracion"] < datetime.now():
        return error_msg(400,"Error: Reserva no valida.",description="El QR expiró.")

    if res["estado_reserva"] != "pendiente":
        return error_msg(400,"Error: Reserva no valida.",description="La reserva no es valida para ser confirmada.")

    try:   
        queries_reservas.actualizar_estado_reserva_por_qr(id_qr_reserva,"finalizada","usado")
    except:
        return error_msg(500,"Error del servidor",description="Ha ocurrido un error en el servidor.")
    return {"msg":"Reserva confirmada exitosamente."},201


def cancelar_reserva_por_mail(id_qr_reserva):
    res  = queries_reservas.obtener_reserva_por_qr(id_qr_reserva)
    if not res:
        return error_msg(404,"Error: reserva no encontrada",description="No existe una reserva con ese ID.")
    
    if res["estado_reserva"] != "pendiente":
        return {"Error":"La reserva no era valida como para ser cancelada."},400

    try:   
        queries_reservas.actualizar_estado_reserva_por_qr(id_qr_reserva,"cancelada")
    except Exception as e:
        return error_msg(500,"Error del servidor",description=f"Ha ocurrido un error en el servidor. {e}")
    return {"msg":"Reserva cancelada exitosamente."},201