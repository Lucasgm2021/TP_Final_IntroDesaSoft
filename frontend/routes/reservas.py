from flask import Blueprint, request, render_template,url_for,jsonify, flash, redirect
from services.reservas import crear_reserva_form_prueba
from datetime import datetime

reserva_bp = Blueprint("reservas",__name__)

@reserva_bp.route("/",methods=["GET","POST"])
def crear_reserva_form():
    if request.method == "GET":
        return render_template("creacion_reserva.html")
    hora = request.form.get('hora', '').strip()
    fecha = request.form.get('fecha', '').strip()
    nro_comensales = int(request.form.get('comensales', 0))
    interior = request.form.get("interior") == "true"
    print("datos del form:",hora,fecha,nro_comensales,interior)
    hora_datetime = datetime.strptime(hora, "%H:%M")
    hora_formateada = hora_datetime.strftime("%H:%M:%S")
    hora_formateada = hora_formateada[0:2] + ":00:00"
    print("hora formateada del form:",hora_formateada)
    resultado = crear_reserva_form_prueba(hora_formateada,fecha,nro_comensales,interior,request.cookies)
    print("resultado en routes despues:", resultado, type(resultado))
    if resultado.get('ok'):
        flash('Reserva creada con exito', 'success')
    else:
        for e in resultado.get('errores', ['Error desconocido.']):
            flash(e, 'error')
    return redirect(url_for('reservas.crear_reserva_form'))