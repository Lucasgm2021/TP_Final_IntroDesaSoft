from flask import Blueprint, request, render_template_string,jsonify
from services import reservas as servicios_reservas
from services.verificaciones import check_usuario_es_admin,check_usuario

reservas_bp = Blueprint("reservas",__name__)

@reservas_bp.route("/", methods=["GET"])
def obtener_reservas():
    is_user, error = check_usuario()

    if not is_user:
        respuesta, status = error
        return jsonify(respuesta), status

    offset = request.args.get("_offset", default=0)
    limit = request.args.get("_limit", default=10)
    fecha = request.args.get("fecha")
    hora = request.args.get("hora")
    estado = request.args.get("estado")
    id_usuario = request.args.get("id_usuario")
    res,status = servicios_reservas.obtener_reservas(offset,limit,fecha,hora,estado,id_usuario)
    return jsonify(res),status

#GET /mesas/disponibles. Sin parametros. Devuelve la cantidad de mesas disponibles en ese momento.
@reservas_bp.route("/mesas/disponibles", methods=["GET"])
def obtener_mesas_disponibles():  
    is_user, error = check_usuario()

    if not is_user:
        respuesta, status = error
        return jsonify(respuesta), status
    res, status =  servicios_reservas.obtener_mesas_disponibles()
    return jsonify(res),status

#GET /mesas/validacion. Parametros: fecha, hora e interior. Devuelve listado desde 1 a una cantidad maxima de comensales que pueden reservar 1 mesa segun la disponibilidad de las mismas segun los parametros.
@reservas_bp.route("/mesas/validacion", methods=["GET"])
def obtener_cantidades_comensales_posibles():
    is_user, error = check_usuario()

    if not is_user:
        respuesta, status = error
        return jsonify(respuesta), status

    fecha = request.args.get("fecha")
    hora = request.args.get("hora")
    interior = request.args.get("interior")
    res,status = servicios_reservas.obtener_cantidades_comensales_posibles(
        fecha,
        hora,
        interior
    )

    return jsonify(res),status
    
@reservas_bp.route("/mostrar_confirmacion", methods=["GET"])
def mostrar_confirmacion_reserva():
    es_admin, error = check_usuario_es_admin()
    if not es_admin:
        respuesta, status = error
        return jsonify(respuesta), status

    id_qr = request.args.get("code")

    html_page = f"""
    <h1>CONFIRMACION DE RESERVA</h1>
    <p>Haga click en el siguiente botón para confirmar la reserva.</p>
    
    <form action="http://localhost:5000/reservas/confirmar/{id_qr}" method="POST">
        <button type="submit" style="padding: 10px 20px; background: green; color: white;">
            Confirmar reserva
        </button>
    </form>
    """
    return render_template_string(html_page,id_qr=id_qr),200
    
@reservas_bp.route("/mostrar_cancelacion", methods=["GET"])
def mostrar_cancelacion_reserva():
    is_user, error = check_usuario()
    if not is_user:
        respuesta, status = error
        return jsonify(respuesta), status

    id_qr = request.args.get("code")

    html_page = f"""
    <h1>CANCELACION DE RESERVA</h1>
    <p>Haga click en el siguiente botón para cancelar la reserva.</p>
    
    <form action="http://localhost:5000/reservas/cancelar/{id_qr}" method="POST">
        <button type="submit" style="padding: 10px 20px; background: green; color: white;">
            Cancelar reserva
        </button>
    </form>
    """
    return render_template_string(html_page,id_qr=id_qr),200

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
    is_user, error = check_usuario()
    if not is_user:
        respuesta, status = error
        return jsonify(respuesta), status

    data = request.get_json()
    res, status = servicios_reservas.modificar_reserva(id_reserva,data)
    return jsonify(res),status