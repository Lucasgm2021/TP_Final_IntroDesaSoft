from flask import Blueprint, render_template

from servicesfront.menu import obtener_menu

menu_bp = Blueprint("menu", __name__)


@menu_bp.route("/")
def mostrar_menu():
    platos = obtener_menu()
    return render_template("menu.html", platos=platos)
