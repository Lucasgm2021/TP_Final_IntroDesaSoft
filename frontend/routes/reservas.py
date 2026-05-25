from flask import Blueprint, request, render_template,url_for,jsonify, flash, redirect
from services.reservas import crear_reserva_form_prueba

reserva_bp = Blueprint("reservas",__name__)

@reserva_bp.route("/",methods=["GET","POST"])
def crear_reserva_form():
    if request.method == "GET":
        return render_template("creacion_reserva.html")
    hora_reserva = request.form.get('hora_reserva', '').strip()
    dia_reserva = request.form.get('dia_reserva', '').strip()
    nro_comensales = int(request.form.get('comensales', 0))
    interior = request.form.get("interior") == "true"

    resultado = crear_reserva_form_prueba(hora_reserva,dia_reserva,nro_comensales,interior)
    print("resultado en routes despues:", resultado, type(resultado))
    if resultado.get('ok'):
        flash('Reserva creada con exito', 'success')
    else:
        for e in resultado.get('errores', ['Error al guardar la nota.']):
            flash(e, 'error')
    
    return redirect(url_for('reservas.crear_reserva_form'))