from flask import Blueprint, request, render_template_string,jsonify
from services import reservas as servicios_reservas
from utiles.messages import error_msg, paginacion_msg

reservas_bp = Blueprint("reservas",__name__)

@reservas_bp.route("/", methods=["GET"])
def obtener_reservas():


    offset = request.args.get("_offset", default=0)
    limit = request.args.get("_limit", default=10)
    fecha = request.args.get("fecha")
    hora = request.args.get("hora")
    estado = request.args.get("estado")

    try:
        reservas, total = servicios_reservas.obtener_reservas(
            offset, limit, fecha, hora, estado
        )
    except ValueError as e:
        return error_msg(400,"Parametros invalidos",description=str(e))
    try:
        reservas, total = servicios_reservas.obtener_reservas(
            offset, limit, fecha, hora, estado
        )
    except ValueError as e:
        return error_msg(400,"Parametros invalidos",description=str(e))
    except Exception as e:
        return error_msg(500,"Error obteniendo reservas",description=str(e))

    return paginacion_msg(
        reservas,
        limit,
        offset,
        total,
        "http://localhost:5000/reservas",
        "reservas",
        200
    )

#GET /mesas/disponibles. Sin parametros. Devuelve la cantidad de mesas disponibles en ese momento.
@reservas_bp.route("/mesas/disponibles", methods=["GET"])
def obtener_mesas_disponibles():

    try:
        mesas_disponibles = servicios_reservas.obtener_mesas_disponibles()
    except Exception as e:
        return error_msg(500,"Error obteniendo mesas disponibles",description=str(e))

    return {
        "mesas_disponibles": mesas_disponibles
    },200

#GET /mesas/validacion. Parametros: fecha y hora. Devuelve listado desde 1 a una cantidad maxima de comensales que pueden reservar 1 mesa segun la disponibilidad de las mismas segun los parametros.
@reservas_bp.route("/mesas/validacion", methods=["GET"])
def obtener_cantidades_comensales_posibles():

    fecha = request.args.get("fecha")
    hora = request.args.get("hora")

    if not fecha or not hora:
        return error_msg(400,"Parametros invalidos","fecha y hora son obligatorios")

    try:
        cantidades = servicios_reservas.obtener_cantidades_comensales_posibles(
            fecha,
            hora
        )
    except ValueError as e:
        return error_msg(400,"Parametros invalidos",description=str(e))
    except Exception as e:
        return error_msg(500,"Error validando mesas",description=str(e))

    return {
        "cantidades_posibles": cantidades
    },200
    
@reservas_bp.route("/mostrar_confirmacion", methods=["GET"])
def mostrar_confirmacion_reserva():
    id_qr = request.args.get("code")

    html_page = f"""
    <h1>CONFIRMACION DE RESERVA</h1>
    <p>Haga click en el siguiente botón para confirmar la reserva.</p>
    
    <form action="/reservas/confirmar/{id_qr}" method="POST">
        <button type="submit" style="padding: 10px 20px; background: green; color: white;">
            Confirmar reserva
        </button>
    </form>
    """
    return render_template_string(html_page,id_qr=id_qr),200
    

#POST /reservas. Recibe json: id_usuario, interior, fecha, hora, nro comensales. Crea una reserva.
@reservas_bp.route("/", methods=["POST"])
def crear_reserva():

    data = request.get_json()

    if not data:
        return error_msg(400,"Body invalido","Debe enviarse JSON")

    try:
        reserva_id = servicios_reservas.crear_reserva(data)
    except ValueError as e:
        return error_msg(400,"Parametros invalidos",description=str(e))
    except Exception as e:
        return error_msg(500,"Error creando reserva",description=str(e))

    return {
        "mensaje": "Reserva creada correctamente",
        "id_reserva": reserva_id
    }, 201

@reservas_bp.route("/confirmar/<id_qr_reserva>",methods=["POST"])
def confirmar_reserva(id_qr_reserva):
    res  = servicios_reservas.obtener_reservas_por_qr(id_qr_reserva)
    
    if not res:
        return jsonify({"Error:":"qr no encontrado"}),404

    if type(res) == dict and res["estado_qr"] != "pendiente":
        return jsonify({"Error:":"qr no valido"}),400
    
    if res["estado_reserva"] != "pendiente":
        return jsonify({"Error:":"Reserva no valida."}),400
    
    try:    
        servicios_reservas.modificar_estado_reserva_por_qr(id_qr_reserva,"finalizada","usado")
    except:
        return error_msg(500,"Error del servidor",description="Ha ocurrido un error en el servidor.")
    return jsonify({"msg":"data actualizada corretamente"}),200

#PATCH /reservas/ Recibe json: estado reserva. Modifica el estado de una reserva.
@reservas_bp.route("/", methods=["PATCH"])
def modificar_estado_reserva():

    data = request.get_json()

    if not data:
        return error_msg(400,"Body invalido","Debe enviarse JSON")

    try:
        servicios_reservas.modificar_estado_reserva(data)
    except ValueError as e:
        return error_msg(400,"Parametros invalidos",description=str(e))
    except Exception as e:
        return error_msg(500,"Error modificando reserva",description=str(e))

    return {
        "mensaje": "Reserva actualizada correctamente"
    },200

    data = request.get_json()

    if not data:
        return error_msg(400,"Body invalido","Debe enviarse JSON")

    try:
        servicios_reservas.modificar_estado_reserva(data)
    except ValueError as e:
        return error_msg(400,"Parametros invalidos",description=str(e))
    except Exception as e:
        return error_msg(500,"Error modificando reserva",description=str(e))

    return {
        "mensaje": "Reserva actualizada correctamente"
    },200