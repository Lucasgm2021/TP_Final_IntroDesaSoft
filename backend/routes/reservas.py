from flask import Blueprint, request
from services import reservas as servicios_reservas
from utiles.messages import error_msg, paginacion_msg
from datetime import datetime

import mysql.connector as mysql

reservas_bp = Blueprint("reservas",__name__)

ESTADOS_RESERVA = ("pendiente","cancelada","finalizada")

#GET /reservas filtros y paginacion. Parametros: estado, fecha y hora.
@reservas_bp.route("/", methods=["GET"])
def obtener_reservas():
    offset = request.args.get("_offset", default=0)
    limit = request.args.get("_limit", default=10)
    fecha = request.args.get("fecha")
    hora = request.args.get("hora")
    estado = request.args.get("estado")

    #validar tipos de datos
    if not str(offset).isnumeric() or not str(limit).isnumeric():
        return error_msg(400,"Parametros incorrectos",description="offset y limit deben ser numeros enteros")
    offset = int(offset)
    limit = int(limit)
    if offset < 0 or limit <= 0:
        return error_msg(400,"Parametros invalidos",description="offset debe ser 0 o mayor y limit debe ser mayor a 0")
    
    total_reservas = servicios_reservas.contar_total_reservas()
    if offset >= total_reservas:
        return error_msg(400,"Parametros invalidos",description="offset no puede ser mayor o igual al total de reservas")
  
    if fecha:
        try:
            fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            return error_msg(400, "Formato de fecha inválido", "INVALID_DATE")

    if hora:
        try:
            fecha_dt = datetime.strptime(hora, "%H:%M:%S")      
        except ValueError:
            return error_msg(400, "Formato de hora inválido", "INVALID_TIME")

    if estado and estado not in ESTADOS_RESERVA:
       return error_msg(400, "Estado inválido", "INVALID_STATE") 

    try:
        reservas = servicios_reservas.obtener_reservas(offset,limit)
    except Exception as e:
        return error_msg(500,"Error obteniendo usuarios.",description=f"Ocurrio un error al intentar obtener usuarios. \n{e}") 
    
    return paginacion_msg(reservas,limit,offset,total_reservas,"http://localhost:5000/reservas","reservas",200)

#GET /mesas/disponibles. Sin parametros. Devuelve la cantidad de mesas disponibles en ese momento.
@reservas_bp.route("/mesas/disponibles", methods=["GET"])
def obtener_mesas_disponibles():
    pass

#GET /mesas/validacion. Parametros: fecha y hora. Devuelve listado desde 1 a una cantidad maxima de comensales que pueden reservar 1 mesa segun la disponibilidad de las mismas segun los parametros.
@reservas_bp.route("/mesas/validacion", methods=["GET"])
def obtener_cantidades_comensales_posibles():
    pass

#POST /reservas. Recibe json: id_usuario, interior, fecha, hora, nro comensales. Crea una reserva.
@reservas_bp.route("/", methods=["POST"])
def crear_reserva():
    return servicios_reservas.crear_reserva()

#PATCH /reservas/ Recibe json: estado reserva. Modifica el estado de una reserva.
@reservas_bp.route("/", methods=["GET"])
def modificar_estado_reserva():
    pass
