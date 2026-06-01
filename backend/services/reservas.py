import os
from flask import session
import uuid
from pathlib import Path
from datetime import datetime,timedelta
import db.reservas as queries_reservas
import db.menu as queries_mesas
import services.mail as servicios_mail
from services.messages import error_msg, error_msg_lista,paginacion_msg
import db.usuarios as queries_usuarios

import db.usuarios as queries_usuarios


ESTADOS_RESERVA = {"pendiente","confirmada","finalizada"}
ESTADOS_QR = {"pendiente","usado","expirado"}
MAS_UNO = 1
CAMPOS_RESERVA_EDITABLES_ADMIN = {"id_mesa","estado_reserva","pendiente_reseña","hora_reserva","fecha","interior","estado_qr","qr_expiracion","comensales"}
CAMPOS_RESERVA_EDITABLES_USUARIO = {"estado_reserva"}
      
def obtener_reservas(offset,limit,fecha,hora,estado,id_usuario):        
    offset = int(offset)
    limit = int(limit)
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
    
    try:
        total_reservas = len(queries_reservas.obtener_reservas(data=data))
        reservas = queries_reservas.obtener_reservas(data=data,limit=limit,offset=offset)
        #fecha es datetime.date, hora es datetime.timedelta y qr_expiracion es datetime.datetime
        reservas = [{**reserva, "fecha": reserva["fecha"].strftime('%Y-%m-%d'),"hora_reserva": str(reserva["hora_reserva"]), "qr_expiracion": str(reserva["qr_expiracion"])}  for reserva in reservas]
    except:
        return error_msg(500,"Error obteniendo reservas",description=f"Ha ocurrido un error en el servidor.")

    return paginacion_msg(
        reservas,
        limit,
        offset,
        total_reservas,
        "http://localhost:5000/reservas",
        "reservas",
        200,
        data
    )
    

    return reservas, total_reservas

def obtener_reserva_con_id(id_reserva):
    try:
        result = queries_reservas.obtener_reserva_por_id(id_reserva)
        if not result:
            return error_msg(404,"Error: reserva no encontrada",description="No existe una reserva con ese ID.")
    except:
        return error_msg(500,"Error obteniendo reserva",description="Ha ocurrido un error en el servidor.")
    reserva = {**result, "fecha": result["fecha"].strftime('%Y-%m-%d'),"hora_reserva": str(result["hora_reserva"]), "qr_expiracion": str(result["qr_expiracion"])}
    return {"data": reserva},200

def obtener_mesas_disponibles():
    #total de mesas - mesas usadas en un determinado momento = mesas disponibles en ese momento
    total_mesas = queries_reservas.obtener_total_mesas()
    mesas_en_uso = queries_reservas.obtener_total_mesas_en_uso()

    mesas_disponibles = total_mesas - mesas_en_uso

    if mesas_disponibles < 0:
        mesas_disponibles = 0

    return {"mesas_disponibles":mesas_disponibles},200

def obtener_cantidades_comensales_posibles(fecha, hora,interior):
    try: 
        capacidades = queries_reservas.obtener_capacidades_mesas_disponibles(
            fecha,
            hora,
            interior
        )
    except:
        return error_msg(500,"Error obteniendo reservas",description="Ha ocurrido un error en el servidor.")

    if not capacidades:
        return {"Msg":"No hay mesas disponibles en esa fecha y hora."},200

    capacidad_maxima = max(capacidades)
    return {"Listado de capacidades disponibles": list(range(1, capacidad_maxima + 1))},200

def crear_reserva(data):
    interior = data.get("interior")
    fecha = data.get("fecha")
    hora = data.get("hora")
    nro_comensales = data.get("nro_comensales")    
    
    if not "id_usuario" in data:
        id_usuario = session["id_usuario"]
    else:
        if data["id_usuario"] != session["id_usuario"] and not session["es_admin"]:
            return error_msg(403,"Permisoos insuficientes",description="No puedes crear una reserva para otro usuario.")
        id_usuario = data["id_usuario"]
    errores = []
    fecha_hora = datetime.strptime(fecha + " " + hora, "%Y-%m-%d %H:%M:%S")
    if fecha_hora <= datetime.now():
        errores.append("Parametros invalidos","La fecha y hora ingresadas no pueden ser anteriores al instante actual.")  
    if ":00:00" not in hora:    
        errores.append("Parametros invalidos","Solo se permiten ingresar horas en punto.")  

    if errores:
        errores = [{"message":"Parametros invalidos","description": error} for error in errores]
        return error_msg_lista(errores,400)  

    ids_mesas = data.get("ids_mesas", [])
    if not ids_mesas:
        return error_msg(400,"Error: No se seleccionaron mesas",description="Debe seleccionar al menos una mesa para crear la reserva.")

    try:
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
        mail_template = Path(__file__).resolve().parent.parent / "templates"/ "mail_reserva.html"
        asunto = "RESERVA REGISTRADA"
        datos_mail = {
            "qr_data": f"http://localhost:5000/reservas/mostrar_confirmacion?code={uuid_qr}",
            "url_cancelar": f"http://localhost:5000/reservas/mostrar_cancelacion?code={uuid_qr}"
        }

        #servicios_mail.enviar_mail_con_qr(mail_usuario,asunto,datos_mail,mail_template)
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