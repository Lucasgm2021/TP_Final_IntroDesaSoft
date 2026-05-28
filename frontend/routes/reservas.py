from flask import Blueprint, request, render_template,url_for,jsonify, flash, redirect
from services.reservas import crear_reserva_form_prueba, obtener_mesas
from datetime import datetime

reserva_bp = Blueprint("reservas",__name__)

@reserva_bp.route("/",methods=["GET","POST"])
def crear_reserva_form():
    if request.method == "GET":
        mesas = None
        fecha = request.args.get("fecha")
        hora = request.args.get("hora")
        ubicacion = request.args.get("ubicacion")
        comensales = request.args.get("comensales")
        numeros_mesas = []
        if fecha and hora and ubicacion and comensales:
            ubicacion_bool = ubicacion == "interior"
            mesas = obtener_mesas(fecha,hora,ubicacion_bool,comensales,request.cookies)
            if mesas.get('errors'):
                for e in resultado.get('errores', ['Error desconocido.']):
                    flash(e, 'error')
                mesas = None
            else:
                mesas = mesas.get("data")
                numeros_mesas = [mesa["numero"] for mesa in mesas]

        return render_template("creacion_reserva.html", mesas=numeros_mesas)

    hora = request.form.get('hora', '').strip()
    fecha = request.form.get('fecha', '').strip()
    nro_comensales = int(request.form.get('comensales', 0))
    interior = request.form.get("ubicacion") == "interior"

    hora_datetime = datetime.strptime(hora, "%H:%M")
    hora_formateada = hora_datetime.strftime("%H:%M:%S")
    hora_formateada = hora_formateada[0:2] + ":00:00"

    resultado = crear_reserva_form_prueba(hora_formateada,fecha,nro_comensales,interior,request.cookies)

    if resultado.get('ok'):
        flash('Reserva creada con exito', 'success')
    else:
        for e in resultado.get('errores', ['Error desconocido.']):
            flash(e, 'error')
    return redirect(url_for('reservas.crear_reserva_form'))

@reserva_bp.route("/example", methods=["GET"])
def ejemplo():
    return render_template("examples/reservas.html")

@reserva_bp.route("/mis_reservas", methods=["GET"])
def mis_reservas():
    return render_template("mis_reservas.html")

@reserva_bp.route("/reservas_admin", methods=["GET"])
def reservas_admin():
    return render_template("reservas_admin.html")

@reserva_bp.route("/home_admin", methods=["GET"])
def home_admin():

    return render_template(
        "home_admin.html",

        mesas_ocupadas=12,
        mesas_totales=30,

        estacionamientos_ocupados=8,
        estacionamientos_totales=20,

        reservas_pendientes=[
            {
                "id_reserva": 1,
                "estado_reserva": "pendiente",
                "nombre_usuario": "Lionel Messi",
                "comensales": 4,
                "fecha": "2026-05-26",
                "hora_reserva": "21:00:00",
                "id_mesa": 12,
                "interior": True
            },
            {
                "id_reserva": 2,
                "estado_reserva": "pendiente",
                "nombre_usuario": "Maria Gomez",
                "comensales": 2,
                "fecha": "2026-05-26",
                "hora_reserva": "22:00:00",
                "id_mesa": 4,
                "interior": False
            }
        ]
    )