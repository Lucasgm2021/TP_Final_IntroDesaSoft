from flask import Blueprint, request, render_template,jsonify
from services import reservas as servicios_reservas
from services.verificaciones import check_usuario_es_admin,check_usuario

reservas_bp = Blueprint("reservas",__name__)

@reservas_bp.route("/", methods=["GET"])
def obtener_reservas():
    is_user, error = check_usuario()

    if not is_user:
        respuesta, status = error
        return jsonify(respuesta), status

    fecha = request.args.get("fecha")
    hora = request.args.get("hora")
    estado = request.args.get("estado")
    id_usuario = request.args.get("id_usuario")
    mesas = request.args.get("mesas","true").lower() == "true"
    res,status = servicios_reservas.obtener_reservas(fecha,hora,estado,id_usuario,mesas)
    return jsonify(res),status


@reservas_bp.route("/<id_reserva>", methods=["GET"])
def obtener_reserva_id(id_reserva):
    is_user, error = check_usuario_es_admin()

    if not is_user:
        respuesta, status = error
        return jsonify(respuesta), status

    res,status = servicios_reservas.obtener_reserva_con_id(id_reserva)
    return jsonify(res),status

#GET /mesas/disponibles. Sin parametros. Devuelve la cantidad de mesas disponibles en ese momento.
@reservas_bp.route("/mesas/disponibles", methods=["GET"])
def obtener_mesas_disponibles():
    res, status =  servicios_reservas.obtener_mesas_disponibles()
    return jsonify(res),status

#GET /mesas/validacion. Parametros: fecha, hora e interior. Devuelve listado desde 1 a una cantidad maxima de comensales que pueden reservar 1 mesa segun la disponibilidad de las mismas segun los parametros.
@reservas_bp.route("/mesas/validacion", methods=["GET"])
def obtener_cantidades_comensales_posibles():
    #is_user, error = check_usuario()

    #if not is_user:
    #    respuesta, status = error
    #    return jsonify(respuesta), status

    fecha = request.args.get("fecha")
    hora = request.args.get("hora")
    interior = request.args.get("interior")
    res,status = servicios_reservas.obtener_cantidades_comensales_posibles(
        fecha,
        hora,
        interior
    )

    return jsonify(res),status

#POST /reservas. Recibe json: id_usuario, interior, fecha, hora, nro comensales. Crea una reserva.
@reservas_bp.route("/", methods=["POST"])
def crear_reserva():
    is_user, error = check_usuario()

    if not is_user:
        respuesta, status = error
        return jsonify(respuesta), status
    
    data = request.get_json()
    
    res,status = servicios_reservas.crear_reserva(data)
    return jsonify(res),status

@reservas_bp.route("/confirmar/<uuid_reserva>",methods=["POST"])
def confirmar_reserva(uuid_reserva):
    es_admin, error = check_usuario_es_admin()
    if not es_admin:
        respuesta, status = error
        return jsonify(respuesta), status 

    res, status = servicios_reservas.confirmar_reserva_por_qr(uuid_reserva)
    return jsonify(res),status

@reservas_bp.route("/cancelar/<uuid_reserva>",methods=["POST"])
def cancelar_reserva(uuid_reserva): 
    is_user, error = check_usuario()
    if not is_user:
        respuesta, status = error
        return jsonify(respuesta), status

    res, status = servicios_reservas.cancelar_reserva_por_mail(uuid_reserva)
    return jsonify(res),status

#PATCH /reservas/ Recibe json: estado reserva. Modifica el estado de una reserva.
@reservas_bp.route("/<id_reserva>", methods=["PATCH"])
def modificar_reserva(id_reserva):
    is_admin, error = check_usuario_es_admin()
    if not is_admin:
        respuesta, status = error
        return jsonify(respuesta), status
    
    data = request.get_json()
    res, status = servicios_reservas.modificar_reserva(id_reserva,data)
    return jsonify(res),status