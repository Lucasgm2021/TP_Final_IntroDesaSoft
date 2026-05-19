from flask import session
import uuid
from pathlib import Path
from datetime import datetime,timedelta
import db.reservas as queries_reservas
import services.mail as servicios_mail
from services.messages import error_msg, paginacion_msg

ESTADOS_RESERVA = {"pendiente","confirmada","cancelada"}
ESTADOS_QR = {"pendiente","usado","expirado"}
MAS_UNO = 1
MENOS_UNO = -1
CAMPOS_RESERVA = {"id_mesa","estado_reserva","pendiente_reseña","hora_reserva","fecha","interior","estado_qr","qr_expiracion","comensales"}
CAMPOS_RESERVA_EDITABLES_USUARIO = {"estado_reserva"}

def obtener_reservas(offset,limit,fecha,hora,estado,id_usuario):
    #validar sesion admin
    if id_usuario and (not id_usuario.isnumeric() or int(id_usuario) <=0):
        return error_msg(400,"Parametros invalidos",description="Id usuario debe ser de tipo entero y mayor a cero.")

    #si el usuario no es admin => valido si intenta buscar info de todos los usuarios o de otro usuario en particular.
    if not session["es_admin"] and (not id_usuario or int(id_usuario) != session["id_usuario"]):
        return error_msg(401,"Usuario no autorizado","Debe ser usuario admin para realizar esta accion")     
        
    #validar tipos
    if not str(offset).isnumeric() or not str(limit).isnumeric():
        return error_msg(400,"Parametros invalidos",description="offset y limit deben ser numeros enteros")
    offset = int(offset)
    limit = int(limit)
    data={}
    if id_usuario:
        id_usuario = int(id_usuario)
        data["id_usuario"] = id_usuario

    if offset < 0 or limit <= 0:
        return error_msg(400,"Parametros invalidos",description="offset debe ser 0 o mayor y limit debe ser mayor a 0")

    # validar fecha
    if fecha:
        try:
            datetime.strptime(fecha,"%Y-%m-%d")
            data["fecha"]=fecha
        except ValueError:
            return error_msg(400,"Parametros invalidos",description="Fecha debe tener formato YYY-mm-dd")

    # validar hora
    if hora:
        try:
            data["hora_reserva"] = hora
            datetime.strptime(hora,"%H:%M:%S")
        except ValueError:
            return error_msg(400,"Parametros invalidos",description="Hora debe tener formato HH:MM")

    # validar estado
    if estado:
        if estado not in ESTADOS_RESERVA:
            return error_msg(400,"Parametros invalidos",description="Estado no valido")
        else:
            data["estado_reserva"] = estado
    try:
        total_reservas = len(queries_reservas.obtener_reservas(data=data))
        if offset >= total_reservas and total_reservas != 0:
            return error_msg(400,"Parametros invalidos",description="offset no puede ser mayor o igual al total de usuarios")
        
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

def obtener_mesas_disponibles():
    #total de mesas - mesas usadas en un determinado momento = mesas disponibles en ese momento
    total_mesas = queries_reservas.obtener_total_mesas()
    mesas_en_uso = queries_reservas.obtener_total_mesas_en_uso()

    mesas_disponibles = total_mesas - mesas_en_uso

    if mesas_disponibles < 0:
        mesas_disponibles = 0

    return {"mesas_disponibles":mesas_disponibles},200

def obtener_cantidades_comensales_posibles(fecha, hora,interior):
    if not fecha or not hora or not interior:
        return error_msg(400,"Parametros invalidos","fecha, hora e interior son obligatorios")
    try:
        datetime.strptime(fecha,"%Y-%m-%d")
        datetime.strptime(hora,"%H:%M:%S")
    except ValueError:
        return error_msg(400,"Parametros invalidos",description="Fecha u hora con formato incorrecto.")

    if interior.lower() not in ("true","false"):
        return error_msg(400,"Parametros invalidos",description="Interior debe ser true or false.")        

    try: 
        capacidades = queries_reservas.obtener_capacidades_mesas_disponibles(
            fecha,
            hora,
            interior
        )
    except:
        return error_msg(500,"Error obteniendo reservas",description="Ha ocurrido un error en el servidor.")

    if not capacidades:
        return jsonify({"Msg":"No hay mesas disponibles en esa fecha y hora."}),200

    capacidad_maxima = max(capacidades)
    return {"Listado de capacidades disponibles": list(range(1, capacidad_maxima + 1))},200

def crear_reserva(data):
    if not data:
        return error_msg(400,"Body invalido","Debe enviarse JSON")
    id_usuario = data.get("id_usuario")
    interior = data.get("interior")
    fecha = data.get("fecha")
    hora = data.get("hora")
    nro_comensales = data.get("nro_comensales")

    #validacion de sesion: usuario reserva solo para si mismo y admin puede para cualquiera.
    if not id_usuario or not isinstance(id_usuario, int) or id_usuario <= 0:
        return error_msg(400,"Parametros invalidos","id_usuario es obligatorio y debe ser de tipo entero positivo.")

    if id_usuario != session["id_usuario"] and not session["es_admin"]:
        return error_msg(401,"Usuario no autorizado","Debe ser usuario admin para realizar esta accion")        

    #validacion de tipos.
    if not fecha or not hora:
        return error_msg(400,"Parametros invalidos","fecha y hora son obligatorios")

    if not nro_comensales or not isinstance(nro_comensales, int):
        return error_msg(400,"Parametros invalidos","nro_comensales es obligatorio o no fue ingresado como entero.")

    if interior is None or not isinstance(interior, bool):
        return error_msg(400,"Parametros invalidos","interior es obligatorio o no fue ingresado como booleano.")

    try:
        datetime.strptime(fecha,"%Y-%m-%d")
        datetime.strptime(hora,"%H:%M:%S")
        time_stamp = fecha + " " + hora
        fecha_hora = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return error_msg(400,"Parametros invalidos",description="Fecha u hora con formato incorrecto.")

    #validacion lógica
    if nro_comensales <= 0:
        return error_msg(400,"Parametros invalidos","nro_comensales debe ser mayor a 0")

    if fecha_hora <= datetime.now():
        return error_msg(400,"Parametros invalidos","La fecha y hora ingresadas no pueden ser anteriores al instante actual.")       

    if ":00:00" not in hora:
        return error_msg(400,"Parametros invalidos","Solo se permiten ingresar horas en punto.")       

    # buscar mesa disponible. Busca una mesa valida no esté en uso en fecha y hora dadas: mesa not in mesas en uso.
    mesa = queries_reservas.obtener_mesa_disponible(
        fecha,
        hora,
        nro_comensales,
        interior
    )

    if not mesa:
        return {"msg":"No hay mesas disponibles para esa cantidad de comensales"},200

    id_mesa = mesa["id_mesa"]
    try:
        #creo reserva
        reserva_id = queries_reservas.insertar_reserva(
            id_usuario
        )

        fecha_hora_mas_30min = fecha_hora + timedelta(minutes=30)
        uuid_qr = str(uuid.uuid4()).replace("-","")

        queries_reservas.insertar_reserva_mesa(
            reserva_id,
            id_mesa,interior,fecha,hora,nro_comensales,uuid_qr,qr_expiracion=fecha_hora_mas_30min
        )
    
        #envío mail. Pendiente servicio de usuarios para obtener mail para enviar notificacion.
        mail_usuario = "lmino@fi.uba.ar"
        mail_template = Path(__file__).resolve().parent / "mail_reserva.html"
        asunto = "RESERVA REGISTRADA"
        datos_mail = {
            "qr_data": f"http://localhost:5000/reservas/mostrar_confirmacion?code={uuid_qr}",
            "url_cancelar": f"http://localhost:5000/reservas/mostrar_cancelacion?code={uuid_qr}"
        }

        servicios_mail.enviar_mail_con_qr(mail_usuario,asunto,datos_mail,mail_template)
        #queries_reservas.actualizar_contadores_reservas_usuario(id_usuario,diferencia_total=MAS_UNO)
    except:
        return error_msg(500,"Error obteniendo reservas",description="Ha ocurrido un error en el servidor.")
    return {"msg":"Reserva creada exitosamente","id": reserva_id},201

def modificar_reserva(id_reserva,data):
    #validar adjunto, que sean ids validos
    if not data:
        return error_msg(400,"Body invalido","Debe enviarse JSON")

    if len(data) > len(CAMPOS_RESERVA) + 1:
        return error_msg(400,"Body invalido","No se puede enviar mas claves que los disponibles.")

    for clave in data:
        if clave not in CAMPOS_RESERVA.add("id_usuario"):
            return error_msg(400,"Body invalido","No se puede enviar una clave que no existe.")

    #validar acciones con permiso admin
    id_usuario = data.get("id_usuario")
    if not id_usuario or not isinstance(id_usuario, int) or id_usuario <= 0:
        return error_msg(400,"Parametros invalidos","id_usuario es obligatorio y debe ser entero mayor a cero.")

    if not session["es_admin"]:
        if id_usuario != session["id_usuario"]:
            return error_msg(401,"Usuario no autorizado","Debe ser usuario admin para realizar esta accion") 

        for clave in data:
            if clave == "id_usuario": continue
            if clave not in CAMPOS_RESERVA_EDITABLES_USUARIO:
                return error_msg(401,"Usuario no autorizado","Debe ser usuario admin para realizar esta accion")
            elif clave=="estado_reserva" and data[clave]!= "cancelada":
                 return error_msg(401,"Usuario no autorizado","Debe ser usuario admin para realizar esta accion")                

    #Validacion de tipos
    if id_mesa and (not isinstance(id_mesa, int) or id_mesa <= 0):
        return error_msg(400,"Parametros invalidos","El id_mesa debe ser de tipo entero positivo.")   
    if estado_reserva and estado_reserva not in ESTADOS_RESERVA:
        return error_msg(400,"Parametros invalidos","El estado_reserva ingresado no es valido.")

    if pendiente_reseña and (not isinstance(pendiente_reseña, bool)):
        return error_msg(400,"Parametros invalidos","El estado_reserva ingresado no es valido.")

    try:
        if hora:
            datetime.strptime(hora,"%H:%M:%S")
        if fecha:
            datetime.strptime(fecha,"%Y-%m-%d")
        if qr_expiracion:
            datetime.strptime(qr_expiracion, "%Y-%m-%d %H:%M:%S")
    except:
        return error_msg(400,"Parametros invalidos","La fecha u hora ingresadas no tienen formato correcto.")

    if interior and (not isinstance(interior, bool)):
        return error_msg(400,"Parametros invalidos","El interior ingresado no es valido.")
    
    if estado_qr and estado_qr not in ESTADOS_QR:
        return error_msg(400,"Parametros invalidos","El estado_reserva ingresado no es valido.")

    if comensales and (not isinstance(comensales, int) or comensales <= 0):
        return error_msg(400,"Parametros invalidos","El nro de comensales debe ser de tipo entero positivo.") 

    #ver si la reserva existe y modificarla.               
    try:
        reserva = queries_reservas.obtener_reserva_por_id(id_reserva)
    except:
        return error_msg(500,"Error obteniendo reserva",description="Ha ocurrido un error en el servidor.")

    if not reserva:
        return error_msg(404,"Error: reserva no encontrada",description="No existe una reserva con ese ID.")
            
    try:
        #estado_anterior = reserva["estado_reserva"]
        queries_reservas.actualizar_reserva(id_reserva,data)
        #Pendiente analizar integridad de contadores de reserva en usuario
        #if estado_reserva in data:
        #    estado_nuevo = queries_reservas.obtener_reserva_por_id(id_reserva)["estado_reserva"]
        #   queries_reservas.actualizar_contadores_reservas_usuario(id_reserva, ?????)

    except:
        return error_msg(500,"Error modificando reservas",description=f"Ha ocurrido un error en el servidor.")

    return {},201

def confirmar_reserva_por_qr(uuid_reserva):
    #validar reserva y qr
    res  = queries_reservas.obtener_reserva_por_qr(uuid_reserva)
    if not res:
        return error_msg(404,"Error: reserva no encontrada",description="No existe una reserva con ese ID.")

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
        queries_reservas.actualizar_estado_reserva_por_qr(uuid_reserva,"cancelada")
        #queries_reservas.actualizar_contadores_reservas_usuario(id_usuario,diferencia_cancelar=MAS_UNO)
    except Exception as e:
        return error_msg(500,"Error del servidor",description=f"Ha ocurrido un error en el servidor. {e}")
    return {"msg":"Reserva cancelada exitosamente."},201