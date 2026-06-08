from flask import (
    Blueprint,
    render_template,
    redirect, session, request
)
from datetime import date, datetime
import requests

from servicesfront.reservas import obtener_reservas_admin
from servicesfront.verificaciones import usuario_es_admin
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
        return redirect("/")

    auth = session.get(FRONTEND_COOKIE_CLAVE) or ""
    hoy = date.today().isoformat()

    r_reservas = requests.get(
        f"{API_BASE_URL}/reservas/",
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )
    todas = r_reservas.json().get("reservas", [])
    reservas_hoy=[]
    for r in todas:
        if r["fecha"] == hoy:
            reservas_hoy.append(r)


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
        f"{API_BASE_URL}/reseñas/todas",
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )
    reseñas_todas = r_reseñas.json().get("data", [])
    pendientes = sum(1 for r in reseñas_todas if r["estado"] == "no_aprobada")
    aprobadas = sum(1 for r in reseñas_todas if r["estado"] == "aprobada")

    r_menu = requests.get(f"{API_BASE_URL}/menu")
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

    auth = session.get(FRONTEND_COOKIE_CLAVE) or ""

    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "editar":
            id_plato = request.form.get("id_plato")
            body = _body_plato(request.form)
            requests.put(
                f"{API_BASE_URL}/menu/{id_plato}",
                json=body,
                cookies={BACKEND_SESSION_COOKIE_NAME: auth}
            )

        elif accion == "crear":
            body = _body_plato(request.form)
            requests.post(
                f"{API_BASE_URL}/menu",
                json=body,
                cookies={BACKEND_SESSION_COOKIE_NAME: auth}
            )

        return redirect("/dashboard/menu")

    eliminar_id = request.args.get("eliminar")
    if eliminar_id:
        requests.delete(
            f"{API_BASE_URL}/menu/{eliminar_id}",
            cookies={BACKEND_SESSION_COOKIE_NAME: auth}
        )
        return redirect("/dashboard/menu")

    response = requests.get(f"{API_BASE_URL}/menu")
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
            f"{API_BASE_URL}/menu/{edit_id}",
            cookies={BACKEND_SESSION_COOKIE_NAME: auth}
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

    auth = session.get(FRONTEND_COOKIE_CLAVE) or ""

    aprobar_id = request.args.get("aprobar")
    desaprobar_id = request.args.get("desaprobar")

    if aprobar_id:
        requests.patch(
            f"{API_BASE_URL}/reseñas/{aprobar_id}",
            json={"estado": "aprobada"},
            cookies={BACKEND_SESSION_COOKIE_NAME: auth}
        )
        return redirect("/dashboard/reseñas")

    if desaprobar_id:
        requests.patch(
            f"{API_BASE_URL}/reseñas/{desaprobar_id}",
            json={"estado": "no_aprobada"},
            cookies={BACKEND_SESSION_COOKIE_NAME: auth}
        )
        return redirect("/dashboard/reseñas")


    response = requests.get(
        f"{API_BASE_URL}/reseñas/todas",
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
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

@dashboard_bp.route("/configuracion", methods=["GET", "POST"])
def configuracion():
    print("ENTRE A CONFIG")
    if not usuario_es_admin():
        return redirect("/")

    auth = session.get(FRONTEND_COOKIE_CLAVE) or ""

    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "editar":
            clave_original = request.form.get("clave_original")

            body = {
                "clave": request.form.get("clave"),
                "valor": request.form.get("valor"),
            }
            requests.patch(
                f"{API_BASE_URL}/info_frontend/{clave_original}",
                json=body,
                cookies={BACKEND_SESSION_COOKIE_NAME: auth}
            )

        elif accion == "crear":
            body = {
                "clave": request.form.get("clave"),
                "valor": request.form.get("valor"),
            }
            requests.post(
                f"{API_BASE_URL}/info_frontend",
                json=body,
                cookies={BACKEND_SESSION_COOKIE_NAME: auth}
            )

        return redirect("/dashboard/configuracion")

    eliminar_clave = request.args.get("eliminar")
    if eliminar_clave:
        requests.delete(
            f"{API_BASE_URL}/info_frontend/{eliminar_clave}",
            cookies={BACKEND_SESSION_COOKIE_NAME: auth}
        )
        return redirect("/dashboard/configuracion")

    response = requests.get(
        f"{API_BASE_URL}/info_frontend",
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
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
            f"{API_BASE_URL}/info_frontend/{edit_clave}",
            cookies={BACKEND_SESSION_COOKIE_NAME: auth}
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
        return redirect("auth.login")

    data = session.get(FRONTEND_COOKIE_CLAVE) or ''

    reservas_todas = obtener_reservas_admin(
        limit=100,
        cookies={BACKEND_SESSION_COOKIE_NAME: data}
    ).get("reservas", [])

    reservas_data = []

    for reserva in reservas_todas:
        reserva_vigente = datetime.strptime(
            reserva["fecha"] + " " + reserva["hora_reserva"],
            "%Y-%m-%d %H:%M:%S"
        ) > datetime.now() and reserva["estado_reserva"] == "pendiente"

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
@dashboard_bp.route("/usuarios", methods=["GET", "POST"])
def usuarios():
    if not usuario_es_admin():
        return redirect("/")

    auth = session.get(FRONTEND_COOKIE_CLAVE) or ""

    response = requests.get(
        f"{API_BASE_URL}/usuarios",
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    )
    users = response.json()["data"]

    usuarios_data = []
    for u in users:
        usuarios_data.append({
            "id": u["email"],
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


@dashboard_bp.route("/mesas", methods=["GET", "POST"])
def mesas():
    if not usuario_es_admin():
        return redirect("/")

    data_sesion = session.get(FRONTEND_COOKIE_CLAVE) or ''

    if request.method == "POST":
        id_mesa = request.form.get("id_mesa")

        body = {
            "numero": int(request.form.get("numero", 0)),
            "capacidad": int(request.form.get("capacidad", request.form.get("comensales", 0))),
            "interior": 1 if "interior" in request.form else 0,
            "funcional": 1 if "funcional" in request.form else 0
        }

        if id_mesa:
            requests.patch(
                f"{API_BASE_URL}/mesas/{id_mesa}",
                json=body,
                cookies={BACKEND_SESSION_COOKIE_NAME: data_sesion}
            )
        else:
            requests.post(
                f"{API_BASE_URL}/mesas",
                json=body,
                cookies={BACKEND_SESSION_COOKIE_NAME: data_sesion}
            )

        return redirect("/dashboard/mesas")

    response = requests.get(
        f"{API_BASE_URL}/mesas",
        cookies={BACKEND_SESSION_COOKIE_NAME: data_sesion}
    )

    data = response.json().get("data", [])

    mesas_lista = []
    for mesa in data:
        id_m = mesa.get("id_mesa", 0)
        num_m = mesa.get("numero", "—")
        cant_m = mesa.get("capacidad", "—")
        int_m = mesa.get("interior", 0)
        func_m = mesa.get("funcional", 0)

        mesas_lista.append({
            "id": id_m,
            "cells": [
                id_m,
                f"Mesa {num_m}",
                f"{cant_m} Personas",
                "Interior" if int_m == 1 or int_m is True else "Exterior",
                "Sí" if func_m == 1 else "No"
            ]
        })

    mesa_editar = None
    crear_nuevo = request.args.get("create")

    edit_id = request.args.get("edit")
    if edit_id:
        response_individual = requests.get(
            f"{API_BASE_URL}/mesas/{edit_id}",
            cookies={BACKEND_SESSION_COOKIE_NAME: data_sesion}
        )
        mesa_editar = response_individual.json().get("data")

    return render_template(
        "dashboard/mesas.html",
        mesas=mesas_lista,
        mesa_editar=mesa_editar,
        crear_nuevo=crear_nuevo
    )


@dashboard_bp.route("/mesas/eliminar/<int:id_mesa>")
def eliminar_mesa_ruta(id_mesa):
    if not usuario_es_admin():
        return redirect("/")

    data_sesion = session.get(FRONTEND_COOKIE_CLAVE) or ''

    requests.delete(
        f"{API_BASE_URL}/mesas/{id_mesa}",
        cookies={BACKEND_SESSION_COOKIE_NAME: data_sesion}
    )

    return redirect("/dashboard/mesas")

