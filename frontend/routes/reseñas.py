from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests
from constants import API_BASE_URL, BACKEND_SESSION_COOKIE_NAME, FRONTEND_COOKIE_CLAVE
from servicesfront.verificaciones import usuario_es_valido
from servicesfront.reseñas import crear_reseña

reseñas_front_bp = Blueprint('reseñas', __name__)

@reseñas_front_bp.route("/", methods=["GET"])
def mostrar_reseñas():
    try:
        respuesta = requests.get(f"{API_BASE_URL}/reseñas")

        if respuesta.status_code == 200:
            lista_de_reseñas = respuesta.json()["data"]
        else:
            lista_de_reseñas = []
    except requests.exceptions.RequestException:
        lista_de_reseñas = []

    return render_template("reseñas/lista_reseñas.html", reseñas=lista_de_reseñas)

@reseñas_front_bp.route("/crear_reseña", methods=["GET","POST"])
def formulario_reseña():
    cookies = {BACKEND_SESSION_COOKIE_NAME: session.get(FRONTEND_COOKIE_CLAVE,"")}
    if not usuario_es_valido():
        return redirect("/")
    
    if request.method=="GET":
        id_reserva = request.args.get("id_reserva")
        valores_clasificacion = [{"id": i, "nombre": f"{i} estrellas"} for i in range(1, 6)] 
        return render_template("reseñas/creacion_reseña.html", id_reserva=id_reserva,valores_clasificacion=valores_clasificacion)
    
    id_reserva = request.form.get("id_reserva")
    if not id_reserva:
        flash("No se ha enviado correctamente la informacion para crear reseña.","error")
        return redirect(url_for("reservas.mis_reservas"))
    
    comentario = request.form.get("comentario")
    calificacion = request.form.get("calificacion")

    resultado = crear_reseña(id_reserva,calificacion,comentario,cookies)

    if resultado.get("ok"):
        flash('Reseña creada con exito', 'success')
    else:
        for e in resultado.get('errores', ['Error desconocido.']):
            flash(e, 'error')        
    return redirect(url_for("reservas.mis_reservas"))


