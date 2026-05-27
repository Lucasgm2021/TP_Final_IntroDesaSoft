from flask import (
    Blueprint,
    render_template,
    redirect, session, request
)
import requests
from servicesfront.verificaciones import usuario_es_admin

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard",
    template_folder="templates/dashboard",
)

@dashboard_bp.route("/")
def home():

    if not usuario_es_admin():
        return redirect()

    return render_template(
        "dashboard/home.html"
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

        data = session.get("usuario") or ''

        requests.put(
            f"http://localhost:5005/menu/{id_plato}",
            json=body,
            cookies={'session': data}
        )

        return redirect("/dashboard/menu")

    response = requests.get(
        "http://localhost:5005/menu"
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
        data = session.get("usuario") or ''
        response = requests.get(
            f"http://localhost:5005/menu/{edit_id}",
            cookies={'session': data}
        )

        plato_editar = response.json()["data"]

    return render_template(
        "dashboard/menu.html",
        menu=menu,
        plato_editar=plato_editar
    )


@dashboard_bp.route("/reservas")
def reservas():

    if not usuario_es_admin():
        return redirect("/")

    data = session.get("usuario") or ''

    response = requests.get(
        f'http://localhost:5005/reservas/',
        cookies={'session': data}
    )

    reservas_todas = response.json()["reservas"]

    reservas_data = []

    for reserva in reservas_todas:
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



    return render_template(
        "dashboard/reservas.html",
        reservas=reservas_data
    )

@dashboard_bp.route("/reseñas")
def reseñas():

    if not usuario_es_admin():
        return redirect("/")

    data = session.get("usuario") or ''

    response = requests.get(
        f'http://localhost:5005/reseñas/todas',
        cookies={'session': data}
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

    data = session.get("usuario") or ''

    response = requests.get(
        f'http://localhost:5005/usuarios',
        cookies={'session': data}
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

    data = session.get("usuario") or ''

    response = requests.get(
        f'http://localhost:5005/info_frontend',
        cookies={'session': data}
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