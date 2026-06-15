from flask import Blueprint, request, render_template,url_for, flash, redirect, session
from servicesfront.reservas import crear_reserva, obtener_mesas, obtener_mis_reservas,cancelar_reserva,confirmar_reserva,obtener_mis_reseñas
from servicesfront.verificaciones import usuario_es_valido,usuario_es_admin
from datetime import datetime
from constants import BACKEND_SESSION_COOKIE_NAME, FRONTEND_COOKIE_CLAVE

reserva_bp = Blueprint("reservas",__name__)

@reserva_bp.route("/",methods=["GET","POST"])
def crear_reserva_form():
    if not usuario_es_valido():
        return redirect(url_for("auth_front.login"))

    cookies = {BACKEND_SESSION_COOKIE_NAME: session.get(FRONTEND_COOKIE_CLAVE,"")}
    if request.method == "GET":
        mesas = None
        fecha = request.args.get("fecha")
        hora = request.args.get("hora")
        ubicacion = request.args.get("ubicacion")
        comensales = request.args.get("comensales")
        mesas_claves_modificadas = []
        horarios = [{"id":f"{hora:02d}:00","nombre":f"{hora:02d}:00"} for hora in range(9, 23)]
        if fecha and hora and ubicacion and comensales:
            ubicacion_bool = ubicacion == "interior"
            mesas = obtener_mesas(fecha,hora,ubicacion_bool,comensales,cookies)
            if mesas.get('errors'):
                for e in mesas.get('errors', ['Error desconocido.']):
                    flash(e, 'error')
                mesas = None
            else:
                mesas = mesas.get("data")
                if not mesas:
                    flash("No hay mesas disponibles para los datos ingresados.", 'info')

            nuevas_claves_dict = {
                "id_mesa": "id",
                "numero": "nombre"
            }
            mesas_claves_modificadas = [
                {nuevas_claves_dict.get(clave, clave): valor for clave, valor in mesa.items()}
                for mesa in mesas
            ]
            for mesa in mesas_claves_modificadas:
                mesa["nombre"] = str(mesa["nombre"]) + " - Capacidad: " + str(mesa["capacidad"])
        return render_template("reservas/creacion_reserva.html", mesas=mesas_claves_modificadas, horarios=horarios)

    hora = request.form.get('hora', '').strip()
    fecha = request.form.get('fecha', '').strip()
    nro_comensales = int(request.form.get('comensales', 0))
    interior = request.form.get("ubicacion") == "interior"
    ids_mesas = request.form.getlist("id_mesas[]")
    hora_datetime = datetime.strptime(hora, "%H:%M")
    hora_formateada = hora_datetime.strftime("%H:%M:%S")
    hora_formateada = hora_formateada[0:2] + ":00:00"

    resultado = crear_reserva(hora_formateada,fecha,nro_comensales,interior,ids_mesas,cookies)

    if resultado.get('ok'):
        flash('Reserva creada con exito', 'success')
    else:
        for e in resultado.get('errores', ['Error desconocido.']):
            flash(e, 'error')
    return redirect(url_for('reservas.crear_reserva_form'))

@reserva_bp.route("/mis_reservas", methods=["GET"])
def mis_reservas():
    if not usuario_es_valido():
        return redirect(url_for("auth_front.login"))

    cookies = {BACKEND_SESSION_COOKIE_NAME: session.get(FRONTEND_COOKIE_CLAVE,"")}
    reservas = obtener_mis_reservas(cookies)
    reseñas = obtener_mis_reseñas(cookies)

    if reservas.get("reservas") is None:
        for e in reservas.get('errores', ['Error desconocido.']):
            flash(e, 'error')
        reservas = []
    else:
        reservas = [{**reserva,"id_reserva": str(reserva["id_reserva"])}for reserva in reservas.get("reservas",[])]
    
    if reseñas.get("data",[]) is None:
        for e in reseñas.get('errores', ['Error desconocido.']):
            flash(e, 'error')
        reseñas = {}
    else:
        reseñas = reseñas.get("data")

    return render_template("reservas/mis_reservas.html", reservas=reservas, reseñas=reseñas)

@reserva_bp.route("/mostrar_confirmacion", methods=["GET"])
def mostrar_confirmacion_reserva():
    if not usuario_es_admin:
        return redirect(url_for("auth_front.login"))

    id_qr = request.args.get("code")
    return render_template("reservas/confirmacion_reserva.html",id_qr=id_qr),200
    
@reserva_bp.route("/mostrar_cancelacion", methods=["GET"])
def mostrar_cancelacion_reserva():
    if not usuario_es_admin:
        return redirect(url_for("auth_front.login"))

    id_qr = request.args.get("code")
    return render_template("reservas/cancelacion_reserva.html",id_qr=id_qr),200

@reserva_bp.route("/cancelar_reserva/<uuid_reserva>", methods=["POST"])
def cancelar_reserva_route(uuid_reserva):
    if not usuario_es_valido():
        return redirect(url_for("auth_front.login"))
    cookies = {BACKEND_SESSION_COOKIE_NAME: session.get(FRONTEND_COOKIE_CLAVE,"")}
    resultado = cancelar_reserva(uuid_reserva, cookies)
    if resultado.get('ok'):
        flash('Reserva cancelada con exito', 'success')
    else:
        for e in resultado.get('errores', ['Error desconocido.']):
            flash(e, 'error')
    return redirect(url_for('reservas.mis_reservas')) 

@reserva_bp.route("/confirmar_reserva/<uuid_reserva>", methods=["POST"])
def confirmar_reserva_route(uuid_reserva):
    if not usuario_es_admin():
        return redirect(url_for("auth_front.login"))
    cookies = {BACKEND_SESSION_COOKIE_NAME: session.get(FRONTEND_COOKIE_CLAVE,"")}
    resultado = confirmar_reserva(uuid_reserva, cookies)
    if resultado.get('ok'):
        flash('Reserva cancelada con exito', 'success')
    else:
        for e in resultado.get('errores', ['Error desconocido.']):
            flash(e, 'error')
    return redirect(url_for('dashboard.home')) 