from flask import (
    Blueprint,
    render_template,
    redirect, session, request
)
from datetime import datetime
import requests
from services.verificaciones import usuario_es_admin
from services.reservas import obtener_reservas_admin, editar_reserva
from constants import API_BASE_URL,BACKEND_SESSION_COOKIE_NAME, FRONTEND_COOKIE_CLAVE

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard",
    template_folder="templates/dashboard",
)

@dashboard_bp.route("/")
def home():

    if not usuario_es_admin():
        return redirect("auth.login")

    cookies = {BACKEND_SESSION_COOKIE_NAME: session.get(FRONTEND_COOKIE_CLAVE) or ''}

    reservas_todas = obtener_reservas_admin(limit=100, cookies=cookies,estado_reserva="pendiente").get("reservas", [])
    reservas_data = []

    for reserva in reservas_todas:
        #filtrar por estado qr y fecha tambien.
        estado_qr_no_vigente = reserva["estado_qr"] != "pendiente"
        qr_expirado = datetime.strptime(reserva["qr_expiracion"], "%Y-%m-%d %H:%M:%S") <= datetime.now()
        reserva_expirada = datetime.strptime(reserva["fecha"] + " " + reserva["hora_reserva"], "%Y-%m-%d %H:%M:%S") <= datetime.now()
        if estado_qr_no_vigente or qr_expirado or reserva_expirada: continue
        reservas_data.append({
            "id": reserva["id_reserva"],
            "cells": [
                reserva["id_reserva"],
                reserva["id_usuario"],
                reserva["estado_reserva"],
                reserva["hora_reserva"],
                reserva["fecha"],
                "Interior" if reserva["interior"] else "Exterior",
                reserva["comensales"],                reserva["id_mesa"],
            ]
        })

    reserva = None

    edit_id = request.args.get("edit")
    if edit_id:
        data = session.get(FRONTEND_COOKIE_CLAVE) or ''
        response = requests.get(
            f'{API_BASE_URL}/reservas/{edit_id}',
            cookies={BACKEND_SESSION_COOKIE_NAME: data}
        )

        reserva = response.json()["data"]
        print("data edit:", edit_id,reserva)
    return render_template(
        "dashboard/home.html",
        reservas=reservas_data,reserva_editar=reserva
    )

@dashboard_bp.route("/menu", methods=["GET", "POST"])
def menu():

    if not usuario_es_admin():
        return redirect("/")

    if request.method == "POST":

        id_plato = request.form.get("id_plato")

        body = {
            "nombre": request.form.get("nombre"),
            "precio": request.form.get("precio"),
            "id_categoria": request.form.get("id_categoria"),
            "link_imagen": request.form.get("link_imagen") or "",
            "hay_stock": "hay_stock" in request.form,
            "gluten": "gluten" in request.form,
            "producto_animal": "producto_animal" in request.form,
            "carnes": "carnes" in request.form,
            "lactosa": "lactosa" in request.form,
        }

        data = session.get(FRONTEND_COOKIE_CLAVE) or ''

        requests.put(
            f'{API_BASE_URL}/menu/{id_plato}',
            json=body,
            cookies={BACKEND_SESSION_COOKIE_NAME: data}
        )

        return redirect("/dashboard/menu")

    response = requests.get(
        f'{API_BASE_URL}/menu'
    )

    data = response.json()["data"]

    menu = []

    for plato in data:

        menu.append({

            "id": plato["id_plato"],

            "cells": [
                plato["id_plato"],
                plato["nombre"],
                plato["id_categoria"],
                f"${plato['precio']}",
                "Sí" if plato["hay_stock"] else "No"
            ]
        })

    plato_editar = None

    edit_id = request.args.get("edit")

    if edit_id:
        data = session.get(FRONTEND_COOKIE_CLAVE) or ''
        response = requests.get(
            f'{API_BASE_URL}/menu/{edit_id}',
            cookies={BACKEND_SESSION_COOKIE_NAME: data}
        )

        plato_editar = response.json()["data"]

    return render_template(
        "dashboard/menu.html",
        menu=menu,
        plato_editar=plato_editar
    )


@dashboard_bp.route("/reservas", methods=["GET","POST"])
def reservas():

    if not usuario_es_admin():
        return redirect("auth.login")

    data = session.get(FRONTEND_COOKIE_CLAVE) or ''

    if request.method == "POST":

        id_reserva = request.form.get("id_reserva")

        body = {
            "estado_reserva": request.form.get("estado_reserva"),
            "fecha": request.form.get("fecha"),
            "hora_reserva": request.form.get("hora_reserva"),
            "comensales": int(request.form.get("comensales")),
            "interior": request.form.get("interior") == "True"
        }

        editar_reserva(
            id_reserva,
            body,
            {BACKEND_SESSION_COOKIE_NAME: data}
        )

        return redirect("/dashboard/reservas")

    reservas_todas = obtener_reservas_admin(
        limit=100,
        cookies={BACKEND_SESSION_COOKIE_NAME: data}
    ).get("reservas", [])

    reservas_data = []

    for reserva in reservas_todas:

        reserva_vigente = (
            datetime.strptime(
                reserva["fecha"] + " " + reserva["hora_reserva"],
                "%Y-%m-%d %H:%M:%S"
            ) > datetime.now()
        )

        if reserva_vigente:
            continue

        reservas_data.append({
            "id": reserva["id_reserva"],
            "cells": [
                reserva["id_reserva"],
                reserva["id_usuario"],
                reserva["estado_reserva"],
                reserva["hora_reserva"],
                reserva["fecha"],
                "Interior" if reserva["interior"] else "Exterior",
                reserva["comensales"],
                reserva["id_mesa"],
            ]
        })

    reserva_editar = None

    edit_id = request.args.get("edit")

    if edit_id:

        response = requests.get(
            f"{API_BASE_URL}/reservas/{edit_id}",
            cookies={BACKEND_SESSION_COOKIE_NAME: data}
        )

        if response.status_code == 200:
            reserva_editar = response.json()["data"]

    return render_template(
        "dashboard/reservas.html",
        reservas=reservas_data,
        reserva_editar=reserva_editar
    )

@dashboard_bp.route("/reseñas")
def reseñas():

    if not usuario_es_admin():
        return redirect("/")

    data = session.get(FRONTEND_COOKIE_CLAVE) or ''

    response = requests.get(
        f'{API_BASE_URL}/reseñas/todas',
        cookies={BACKEND_SESSION_COOKIE_NAME: data}
    )

    reseñas = response.json()["data"]

    resenias = []

    for reseña in reseñas:
        resenias.append({

            "id": reseña["id_reseña"],

            "cells": [

                reseña["id_reseña"],
                reseña["id_reserva"],
                reseña["comentario"],
                reseña["calificacion"],
                reseña["estado"],
                reseña["id_usuario"],
                reseña["email"]

            ]
        })



    return render_template(
        "dashboard/reseñas.html",
        resenias=resenias
    )


@dashboard_bp.route("/usuarios")
def usuarios():

    if not usuario_es_admin():
        return redirect("/")

    data = session.get(FRONTEND_COOKIE_CLAVE) or ''

    response = requests.get(
        f'{API_BASE_URL}/usuarios',
        cookies={BACKEND_SESSION_COOKIE_NAME: data}
    )

    users = response.json()["data"]

    usuarios_data = []

    for usuario in users:
        usuarios_data.append({

            "id": usuario["id_usuario"],

            "cells": [
                usuario["id_usuario"],
                usuario["email"],
                'Si' if usuario["es_admin"] == 1 else 'No',

            ]
        })



    return render_template(
        "dashboard/usuarios.html",
        usuarios=usuarios_data
    )

@dashboard_bp.route("/configuracion/")
def configuracion():

    if not usuario_es_admin():
        return redirect("/")

    data = session.get(FRONTEND_COOKIE_CLAVE) or ''

    response = requests.get(
        f'{API_BASE_URL}/info_frontend',
        cookies={BACKEND_SESSION_COOKIE_NAME: data}
    )

    informacion = response.json()["data"]

    infos = []

    for info in informacion:
        infos.append({

            "id": info["clave"],

            "cells": [
                info["clave"],
                info["valor"],

            ]
        })



    return render_template(
        "dashboard/info-dash.html",
        infodash=infos
    )