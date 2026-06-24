import os
from flask import session
import uuid
from pathlib import Path
from datetime import datetime,timedelta
from datetime import time, date, datetime
from zoneinfo import ZoneInfo

import db.reservas as queries_reservas
import db.menu as queries_mesas
import services.mail as servicios_mail
from services.messages import error_msg, error_msg_lista
from services.mesas import obtener_mesas
import db.usuarios as queries_usuarios
from constants import URL_PAGINA_WEB,SERVICIO_MAIL,SERVICIO_MAIL_GMAIL_APP_PASS,SERVICIO_MAIL_MAILJET

MAS_UNO = 1

def obtener_reservas(fecha,hora,estado,id_usuario,mesas):        
    data={}
    if not "id_usuario" in data:
        if not session["es_admin"]:
            id_usuario = session["id_usuario"]
    else:
        if data["id_usuario"] != session["id_usuario"] and not session["es_admin"]:
            return error_msg(403,"Permisoos insuficientes",description="No puedes crear una reserva para otro usuario.")
        id_usuario = data["id_usuario"]

    if id_usuario:
        id_usuario = int(id_usuario)
        data["id_usuario"] = id_usuario    

    if fecha:
        data["fecha"]=fecha
    
    if hora:
        data["hora_reserva"]=hora
        
    if estado:
        data["estado_reserva"]=estado
    data["mesas"] = mesas
    try:
        reservas = queries_reservas.obtener_reservas(data=data)
        #fecha es datetime.date, hora es datetime.timedelta y qr_expiracion es datetime.datetime
        reservas = [{**reserva, "fecha": reserva["fecha"].strftime('%Y-%m-%d'),"hora_reserva": str(reserva["hora_reserva"]), "qr_expiracion": str(reserva["qr_expiracion"])}  for reserva in reservas]
    except:
        return error_msg(500,"Error obteniendo reservas",description=f"Ha ocurrido un error en el servidor.")

    return {"reservas": reservas},200

def obtener_reserva_con_id(id_reserva):
    try:
        result = queries_reservas.obtener_reserva_por_id(id_reserva)
        if not result:
            return error_msg(404,"Error: reserva no encontrada",description="No existe una reserva con ese ID.")
    except:
        return error_msg(500,"Error obteniendo reserva",description="Ha ocurrido un error en el servidor.")
    reserva = {**result, "fecha": result["fecha"].strftime('%Y-%m-%d'),"hora_reserva": str(result["hora_reserva"]), "qr_expiracion": str(result["qr_expiracion"])}
    return {"data": reserva},200

def crear_reserva(data):
    interior = data.get("interior")
    fecha = data.get("fecha")
    hora = data.get("hora")
    nro_comensales = data.get("nro_comensales")    
    ids_mesas = data.get("ids_mesas", [])
    if not "id_usuario" in data:
        id_usuario = session["id_usuario"]
    else:
        if data["id_usuario"] != session["id_usuario"] and not session["es_admin"]:
            return error_msg(403,"Permisoos insuficientes",description="No puedes crear una reserva para otro usuario.")
        id_usuario = data["id_usuario"]

    ahora_arg = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
    instante_actual = ahora_arg.time()
    hoy = ahora_arg.date().isoformat()
    hora_datetime = time.fromisoformat(hora)

    if fecha == hoy and hora_datetime < instante_actual: 
        return error_msg(400,"Solicitud invalida",description="No puedes reservar hoy antes que la hora actual.")

    fecha_hora = datetime.strptime(fecha + " " + hora, "%Y-%m-%d %H:%M:%S")

    try:
        mesas = obtener_mesas()
        capacidades = sorted([mesa["capacidad"] for mesa in mesas if str(mesa["id_mesa"]) in ids_mesas], reverse=True) #ordeno de mayor a menor capacidad.
        #Reviso que la cantidad de comensales minimo requiera a todas las mesas menos la mas chica + 1.
        if nro_comensales < sum(capacidades[:len(capacidades)-1])+1:
            return error_msg(400,"Error: Capacidad excedida",description=f"La capacidad de las mesas seleccionadas sobrepasa la cantidad de comensales.")
        
        #Reviso que la cantidad de comensales maximo no exceda la capacidad total de las mesas seleccionadas.
        if nro_comensales > sum(capacidades):
            return error_msg(400,"Error: Capacidad insuficiente",description=f"La capacidad total de las mesas seleccionadas es {sum(capacidades)}, pero se necesitan {nro_comensales} para acomodar a todos los comensales.")

        fecha_hora_mas_30min = fecha_hora + timedelta(minutes=30)
        uuid_qr = str(uuid.uuid4()).replace("-","")
        #creo reserva
        id_reserva = queries_reservas.insertar_reserva(
            interior,id_usuario,fecha,hora,nro_comensales,uuid_qr,qr_expiracion=fecha_hora_mas_30min
        )
        for id_mesa in ids_mesas:
            queries_reservas.insertar_reserva_mesa(
                id_reserva,
                id_mesa
            )
        #envío mail. 
        mail_usuario = queries_usuarios.obtener_usuario_id(id_usuario)["email"]
        asunto = "RESERVA REGISTRADA"
        
        datos_mail = {
            "qr_data": f"{URL_PAGINA_WEB}/reservas/mostrar_confirmacion?code={uuid_qr}",
            "url_cancelar": f"{URL_PAGINA_WEB}/reservas/mostrar_cancelacion?code={uuid_qr}"
        }

        mail_template = Path(__file__).resolve().parent.parent / "templates"/ "mail_reserva_qr_adjunto.html"

        servicios_mail.enviar_mail_con_qr(
            proveedor=SERVICIO_MAIL,mail_destino=mail_usuario,
            asunto=asunto,mail_data=datos_mail,ruta_template=mail_template
        )  
        queries_reservas.actualizar_contadores_reservas_usuario(id_usuario,diferencia_total=MAS_UNO)
    except Exception as e:
        return error_msg(500,"Error creando la reserva",description=f"Ha ocurrido un error en el servidor. {e}")
    return {"msg":"Reserva creada exitosamente","id": id_reserva},201

def modificar_reserva(id_reserva,data):
    #validar acciones con permiso admin
    id_usuario = data.get("id_usuario")

    try:
        reserva = queries_reservas.obtener_reserva_mesa_por_id(id_reserva)
    except:
        return error_msg(500,"Error obteniendo reserva",description="Ha ocurrido un error en el servidor.")

    if not reserva:
        return error_msg(404,"Error: reserva no encontrada",description="No existe una reserva con ese ID.")
            
    try:
        queries_reservas.actualizar_reserva(id_reserva,data)
        if not session["es_admin"]:
            #usuario comun solo puede cancelar su propia reserva como accion en este endpoint.
            queries_reservas.actualizar_contadores_reservas_usuario(id_usuario,diferencia_cancelar=MAS_UNO)            
    except:
        return error_msg(500,"Error modificando reservas",description="Ha ocurrido un error en el servidor.")

    return {},201

def confirmar_reserva_por_qr(uuid_reserva):
    #validar reserva y qr
    res  = queries_reservas.obtener_reserva_por_qr(uuid_reserva)
    if res["estado_qr"] != "pendiente":
        return error_msg(400,"Error: Reserva no valida.",description="El QR ya fue leido o expiró.")

    if res["qr_expiracion"] < datetime.now():
        return error_msg(400,"Error: Reserva no valida.",description="El QR expiró.")

    if res["estado_reserva"] != "pendiente":
        return error_msg(400,"Error: Reserva no valida.",description="La reserva no es valida para ser confirmada.")

    try:   
        queries_reservas.actualizar_estado_reserva_por_qr(uuid_reserva,"finalizada","usado")
    except:
        return error_msg(500,"Error del servidor",description="Ha ocurrido un error en el servidor.")
    return {"msg":"Reserva confirmada exitosamente."},201

def cancelar_reserva_por_mail(uuid_reserva):
    #validar reserva
    res  = queries_reservas.obtener_reserva_por_qr(uuid_reserva)
    if not res:
        return error_msg(404,"Error: reserva no encontrada",description="No existe una reserva con ese ID.")
    
    if res["estado_reserva"] != "pendiente":
        return {"Error":"La reserva no era valida como para ser cancelada."},400

    try:
        id_usuario = queries_reservas.obtener_reserva_por_id(res["id_reserva"])["id_usuario"]
        queries_reservas.actualizar_estado_reserva_por_qr(uuid_reserva,"cancelada")
        queries_reservas.actualizar_contadores_reservas_usuario(id_usuario,diferencia_cancelar=MAS_UNO)
    except:
        return error_msg(500,"Error del servidor",description="Ha ocurrido un error en el servidor.")
    return {"msg":"Reserva cancelada exitosamente."},201