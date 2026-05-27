from flask import (
    Blueprint,
    render_template,
    redirect
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

    #if not usuario_es_admin():
    #    return redirect("/")

    return render_template(
        "dashboard/home.html"
    )

@dashboard_bp.route("/reservas")
def reservas():

    #if not usuario_es_admin():
    #    return redirect("/")

    return render_template(
        "dashboard/reservas.html"
    )

@dashboard_bp.route("/menu")
def menu():

    #if not usuario_es_admin():
    #    return redirect("/")

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



    return render_template(
        "dashboard/menu.html",
        menu=menu
    )


