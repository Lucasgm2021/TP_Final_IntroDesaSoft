from flask import Blueprint, render_template, redirect, session, request
from datetime import date

import servicesfront.dashboard as svs
from servicesfront.reservas import obtener_reservas_admin
from servicesfront.verificaciones import usuario_es_admin
from constants import BACKEND_SESSION_COOKIE_NAME, FRONTEND_COOKIE_CLAVE

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

    todas = svs.obtener_todas_las_reservas(auth)
    reservas_hoy = [r for r in todas if r["fecha"] == hoy]

    reservas_rows = [
        {
            "id": r["id_reserva"],
            "cells": [
                r["id_reserva"],
                r["hora_reserva"],
                r["comensales"],
                "Interior" if r["interior"] else "Exterior",
                r["estado_reserva"],
            ]
        }
        for r in reservas_hoy
    ]

    reseñas_todas = svs.obtener_todas_las_reseñas(auth)
    pendientes = sum(1 for r in reseñas_todas if r["estado"] == "no_aprobada")
    aprobadas  = sum(1 for r in reseñas_todas if r["estado"] == "aprobada")

    platos    = svs.obtener_menu()
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
            svs.editar_plato(request.form.get("id_plato"), svs.build_body_plato(request.form), auth)
        elif accion == "crear":
            svs.crear_plato(svs.build_body_plato(request.form), auth)
        return redirect("/dashboard/menu")

    eliminar_id = request.args.get("eliminar")
    if eliminar_id:
        svs.eliminar_plato(eliminar_id, auth)
        return redirect("/dashboard/menu")

    data = svs.obtener_menu()

    menu_rows = [
        {
            "id": p["id_plato"],
            "cells": [
                p["id_plato"],
                p["nombre"],
                p["id_categoria"],
                f"${p['precio']}",
                "Sí" if p["hay_stock"] else "No",
            ]
        }
        for p in data
    ]

    plato_editar = None
    edit_id = request.args.get("edit")
    if edit_id:
        plato_editar = svs.obtener_plato(edit_id, auth)

    return render_template(
        "dashboard/menu.html",
        menu=menu_rows,
        plato_editar=plato_editar,
        nuevo="nueva" in request.args,
    )


@dashboard_bp.route("/reseñas")
def reseñas():
    if not usuario_es_admin():
        return redirect("/")

    auth = session.get(FRONTEND_COOKIE_CLAVE) or ""

    aprobar_id    = request.args.get("aprobar")
    desaprobar_id = request.args.get("desaprobar")

    if aprobar_id:
        svs.aprobar_reseña(aprobar_id, auth)
        return redirect("/dashboard/reseñas")

    if desaprobar_id:
        svs.desaprobar_reseña(desaprobar_id, auth)
        return redirect("/dashboard/reseñas")

    reseñas_data = svs.obtener_todas_las_reseñas(auth)

    resenias = [
        {
            "id":      reseña["id_resenia"],
            "checked": reseña["estado"] == "aprobada",
            "cells": [
                reseña["id_resenia"],
                reseña["id_reserva"],
                reseña["comentario"],
                reseña["calificacion"],
                reseña["id_usuario"],
                reseña["email"],
            ]
        }
        for reseña in reseñas_data
    ]

    return render_template("dashboard/reseñas.html", resenias=resenias)


@dashboard_bp.route("/configuracion/", methods=["GET", "POST"])
def configuracion():
    if not usuario_es_admin():
        return redirect("/")

    auth = session.get(FRONTEND_COOKIE_CLAVE) or ""

    if request.method == "POST":
        accion = request.form.get("accion")
        body   = {"clave": request.form.get("clave"), "valor": request.form.get("valor")}
        if accion == "editar":
            svs.editar_info_frontend(request.form.get("clave_original"), body, auth)
        elif accion == "crear":
            svs.crear_info_frontend(body, auth)
        return redirect("/dashboard/configuracion")

    eliminar_clave = request.args.get("eliminar")
    if eliminar_clave:
        svs.eliminar_info_frontend(eliminar_clave, auth)
        return redirect("/dashboard/configuracion")

    informacion = svs.obtener_info_frontend(auth)

    infos = [
        {
            "id": info["clave"],
            "cells": [info["clave"], info["valor"]],
        }
        for info in informacion
    ]

    info_editar = None
    edit_clave  = request.args.get("edit")
    if edit_clave:
        info_editar = svs.obtener_info_frontend_por_clave(edit_clave, auth)

    return render_template(
        "dashboard/info-dash.html",
        infodash=infos,
        info_editar=info_editar,
        nueva="nueva" in request.args,
    )


@dashboard_bp.route("/reservas", methods=["GET", "POST"])
def reservas():
    if not usuario_es_admin():
        return redirect("auth.login")

    auth = session.get(FRONTEND_COOKIE_CLAVE) or ""

    reservas_todas = obtener_reservas_admin(
        limit=100,
        cookies={BACKEND_SESSION_COOKIE_NAME: auth}
    ).get("reservas", [])

    reservas_data = [
        {
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
        }
        for r in reservas_todas
    ]

    return render_template("dashboard/reservas.html", reservas=reservas_data)


@dashboard_bp.route("/usuarios", methods=["GET", "POST"])
def usuarios():
    if not usuario_es_admin():
        return redirect("/")

    auth  = session.get(FRONTEND_COOKIE_CLAVE) or ""
    users = svs.obtener_usuarios(auth)

    usuarios_data = [
        {
            "id": u["email"],
            "cells": [
                u["id_usuario"],
                u["email"],
                "Sí" if u["es_admin"] == 1 else "No",
            ]
        }
        for u in users
    ]

    return render_template("dashboard/usuarios.html", usuarios=usuarios_data)


@dashboard_bp.route("/mesas", methods=["GET", "POST"])
def mesas():
    if not usuario_es_admin():
        return redirect("/")

    auth = session.get(FRONTEND_COOKIE_CLAVE) or ""

    if request.method == "POST":
        id_mesa = request.form.get("id_mesa")
        body    = svs.build_body_mesa(request.form)
        if id_mesa:
            svs.editar_mesa(id_mesa, body, auth)
        else:
            svs.crear_mesa(body, auth)
        return redirect("/dashboard/mesas")

    data = svs.obtener_mesas(auth)

    mesas_lista = [
        {
            "id": m.get("id_mesa", 0),
            "cells": [
                m.get("id_mesa", 0),
                f"Mesa {m.get('numero', '—')}",
                f"{m.get('capacidad', '—')} Personas",
                "Interior" if m.get("interior") in (1, True) else "Exterior",
                "Sí" if m.get("funcional") == 1 else "No",
            ]
        }
        for m in data
    ]

    mesa_editar = None
    edit_id     = request.args.get("edit")
    if edit_id:
        mesa_editar = svs.obtener_mesa(edit_id, auth)

    return render_template(
        "dashboard/mesas.html",
        mesas=mesas_lista,
        mesa_editar=mesa_editar,
        crear_nuevo=request.args.get("create"),
    )


@dashboard_bp.route("/mesas/eliminar/<int:id_mesa>")
def eliminar_mesa_ruta(id_mesa):
    if not usuario_es_admin():
        return redirect("/")

    auth = session.get(FRONTEND_COOKIE_CLAVE) or ""
    svs.eliminar_mesa(id_mesa, auth)
    return redirect("/dashboard/mesas")