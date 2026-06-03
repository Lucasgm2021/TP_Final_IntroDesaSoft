from flask import (
    Blueprint,
    render_template,
    redirect, session, request
)
from datetime import date
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
        return redirect("/")

    auth = session.get("usuario") or ""
    hoy = date.today().isoformat()

    r_reservas = requests.get(
        f"http://127.0.0.1:5005/reservas/",
        cookies={"session": auth}
    )
    todas = r_reservas.json().get("reservas", [])
    reservas_hoy = [r for r in todas if r["fecha"] == hoy]

    reservas_rows = []
    for r in reservas_hoy:
        reservas_rows.append({
            "id": r["id_reserva"],
            "cells": [
                r["id_reserva"],
                r["hora_reserva"],
                r["comensales"],
                "Interior" if r["interior"] else "Exterior",
                r["estado_reserva"],
            ]
        })

    r_reseñas = requests.get(
        "http://127.0.0.1:5005/reseñas/todas",
        cookies={"session": auth}
    )
    reseñas_todas = r_reseñas.json().get("data", [])
    pendientes = sum(1 for r in reseñas_todas if r["estado"] == "no_aprobada")
    aprobadas = sum(1 for r in reseñas_todas if r["estado"] == "aprobada")

    r_menu = requests.get("http://127.0.0.1:5005/menu")
    platos = r_menu.json().get("data", [])
    sin_stock = sum(1 for p in platos if not p["hay_stock"])

    return render_template(
        "dashboard/home.html",
        reservas_hoy=reservas_rows,
        fecha_hoy=hoy,
        pendientes=pendientes,
        aprobadas=aprobadas,
        sin_stock=sin_stock,
    )


@dashboard_bp.route("/menu", methods=["GET", "POST"])
def menu():
    if not usuario_es_admin():
        return redirect("/")

    auth = session.get("usuario") or ""

    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "editar":
            id_plato = request.form.get("id_plato")
            body = _body_plato(request.form)
            requests.put(
                f"http://127.0.0.1:5005/menu/{id_plato}",
                json=body,
                cookies={"session": auth}
            )

        elif accion == "crear":
            body = _body_plato(request.form)
            requests.post(
                "http://127.0.0.1:5005/menu",
                json=body,
                cookies={"session": auth}
            )

        return redirect("/dashboard/menu")

    eliminar_id = request.args.get("eliminar")
    if eliminar_id:
        requests.delete(
            f"http://127.0.0.1:5005/menu/{eliminar_id}",
            cookies={"session": auth}
        )
        return redirect("/dashboard/menu")

    response = requests.get("http://127.0.0.1:5005/menu")
    data = response.json()["data"]

    menu_rows = []
    for plato in data:
        menu_rows.append({
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
        r = requests.get(
            f"http://127.0.0.1:5005/menu/{edit_id}",
            cookies={"session": auth}
        )
        plato_editar = r.json()["data"]

    nueva = "nueva" in request.args

    return render_template(
        "dashboard/menu.html",
        menu=menu_rows,
        plato_editar=plato_editar,
        nuevo=nueva
    )

def _body_plato(form):
    return {
        "nombre":          form.get("nombre"),
        "precio":          int(float(form.get("precio", 0))),
        "id_categoria":    int(form.get("id_categoria", 0)),
        "link_imagen":     form.get("link_imagen") or "",
        "hay_stock":       "hay_stock"       in form,
        "gluten":          "gluten"          in form,
        "producto_animal": "producto_animal" in form,
        "carnes":          "carnes"          in form,
        "lactosa":         "lactosa"         in form,
    }

@dashboard_bp.route("/reseñas")
def reseñas():
    if not usuario_es_admin():
        return redirect("/")

    auth = session.get("usuario") or ""

    aprobar_id = request.args.get("aprobar")
    desaprobar_id = request.args.get("desaprobar")

    if aprobar_id:
        requests.patch(
            f"http://127.0.0.1:5005/reseñas/{aprobar_id}",
            json={"estado": "aprobada"},
            cookies={"session": auth}
        )
        return redirect("/dashboard/reseñas")

    if desaprobar_id:
        requests.patch(
            f"http://127.0.0.1:5005/reseñas/{desaprobar_id}",
            json={"estado": "no_aprobada"},
            cookies={"session": auth}
        )
        return redirect("/dashboard/reseñas")


    response = requests.get(
        "http://127.0.0.1:5005/reseñas/todas",
        cookies={"session": auth}
    )
    reseñas_data = response.json()["data"]

    resenias = []
    for reseña in reseñas_data:
        resenias.append({
            "id": reseña["id_reseña"],
            "checked": reseña["estado"] == "aprobada",
            "cells": [
                reseña["id_reseña"],
                reseña["id_reserva"],
                reseña["comentario"],
                reseña["calificacion"],
                reseña["id_usuario"],
                reseña["email"],
            ]
        })

    return render_template(
        "dashboard/reseñas.html",
        resenias=resenias
    )

@dashboard_bp.route("/configuracion/", methods=["GET", "POST"])
def configuracion():
    if not usuario_es_admin():
        return redirect("/")

    auth = session.get("usuario") or ""

    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "editar":
            clave_original = request.form.get("clave_original")
            body = {
                "clave": request.form.get("clave"),
                "valor": request.form.get("valor"),
            }
            requests.patch(
                f"http://127.0.0.1:5005/info_frontend/{clave_original}",
                json=body,
                cookies={"session": auth}
            )

        elif accion == "crear":
            body = {
                "clave": request.form.get("clave"),
                "valor": request.form.get("valor"),
            }
            requests.post(
                "http://127.0.0.1:5005/info_frontend",
                json=body,
                cookies={"session": auth}
            )

        return redirect("/dashboard/configuracion/")

    eliminar_clave = request.args.get("eliminar")
    if eliminar_clave:
        requests.delete(
            f"http://127.0.0.1:5005/info_frontend/{eliminar_clave}",
            cookies={"session": auth}
        )
        return redirect("/dashboard/configuracion/")

    response = requests.get(
        "http://127.0.0.1:5005/info_frontend",
        cookies={"session": auth}
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

    info_editar = None
    edit_clave = request.args.get("edit")
    if edit_clave:
        r = requests.get(
            f"http://127.0.0.1:5005/info_frontend/{edit_clave}",
            cookies={"session": auth}
        )
        valor = r.json().get(edit_clave)
        if valor is not None:
            info_editar = {"clave": edit_clave, "valor": valor}

    nueva = "nueva" in request.args

    return render_template(
        "dashboard/info-dash.html",
        infodash=infos,
        info_editar=info_editar,
        nueva=nueva
    )

@dashboard_bp.route("/reservas", methods=["GET", "POST"])
def reservas():
    if not usuario_es_admin():
        return redirect("/")

    auth = session.get("usuario") or ""

    response = requests.get(
        "http://127.0.0.1:5005/reservas/",
        cookies={"session": auth}
    )
    reservas_todas = response.json()["reservas"]

    reservas_data = []
    for r in reservas_todas:
        reservas_data.append({
            "id": r["id_reserva"],
            "cells": [
                r["id_reserva"],
                r["id_usuario"],
                r["estado_reserva"],
                r["hora_reserva"],
                r["fecha"],
                "Interior" if r["interior"] else "Exterior",
                r["comensales"],
                r["id_mesa"],
            ]
        })

    return render_template(
        "dashboard/reservas.html",
        reservas=reservas_data,
    )

def _body_reserva(form):
    return {
        "id_usuario":     form.get("id_usuario"),
        "estado_reserva": form.get("estado_reserva"),
        "hora_reserva":   form.get("hora_reserva"),
        "fecha":          form.get("fecha"),
        "interior":       "interior" in form,
        "comensales":     form.get("comensales"),
        "id_mesa":        form.get("id_mesa"),
    }


@dashboard_bp.route("/usuarios", methods=["GET", "POST"])
def usuarios():
    if not usuario_es_admin():
        return redirect("/")

    auth = session.get("usuario") or ""

    response = requests.get(
        "http://127.0.0.1:5005/usuarios",
        cookies={"session": auth}
    )
    users = response.json()["data"]

    usuarios_data = []
    for u in users:
        usuarios_data.append({
            "id": u["id_usuario"],
            "cells": [
                u["id_usuario"],
                u["email"],
                "Sí" if u["es_admin"] == 1 else "No",
            ]
        })


    return render_template(
        "dashboard/usuarios.html",
        usuarios=usuarios_data,
    )

def _body_usuario(form):
    body = {
        "email":    form.get("email"),
        "es_admin": "es_admin" in form,
    }
    password = form.get("password")
    if password:
        body["password"] = password
    return body
