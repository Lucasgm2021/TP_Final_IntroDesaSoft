from flask import Blueprint, render_template

from servicesfront.menu import obtener_menu

public_bp = Blueprint("public", __name__)


@public_bp.route("/menu")
def menu():
    platos = obtener_menu()
    return render_template("menu.html", platos=platos)
