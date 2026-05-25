from flask import Blueprint, request, render_template,url_for,jsonify
from services.reservas import crear_reserva_form_prueba

reserva_bp = Blueprint("reservas",__name__)

@reserva_bp.route("/",methods=["GET","POST"])
def crear_reserva_form():
    if request.method == "GET":
        return render_template("creacion_reserva.html")
    print("Aqui llega")
    hora_reserva = request.form.get('hora_reserva', '').strip()
    dia_reserva = request.form.get('dia_reserva', '').strip()
    nro_comensales = int(request.form.get('comensales', 0))
    interior = request.form.get("interior") == "true"

    data = (hora_reserva,dia_reserva,nro_comensales,interior)
    for dato in data:
        print(dato,type(dato))
    
    return jsonify({"msg":"todo ok","data":data}),201