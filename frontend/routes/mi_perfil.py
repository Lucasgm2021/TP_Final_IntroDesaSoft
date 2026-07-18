from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from servicesfront.mi_perfil import eliminar_mi_perfil, obtener_mi_perfil, actualizar_mi_perfil
from servicesfront.verificaciones import usuario_es_valido
from constants import BACKEND_SESSION_COOKIE_NAME, FRONTEND_COOKIE_CLAVE

usuarios_bp = Blueprint(
    "usuarios",
    __name__
)

@usuarios_bp.route("/cliente/mi_perfil", methods=["GET", "POST"])
def mi_perfil():
    if not usuario_es_valido():
        return redirect(url_for("auth.login"))

    cookies = {BACKEND_SESSION_COOKIE_NAME: session.get(FRONTEND_COOKIE_CLAVE,"")}
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        respuesta = actualizar_mi_perfil(email, password, cookies)

        if respuesta.get("message",""):
            flash(respuesta.get("message"), "success")
            return redirect(url_for("usuarios.mi_perfil"))
        else:
            flash(respuesta.get("error", "Error al actualizar"), "error")
            return redirect(url_for("usuarios.mi_perfil"))
    
    usuario = obtener_mi_perfil(cookies)
    return render_template("mi_perfil.html",usuario=usuario)

@usuarios_bp.route("/cliente/mi_perfil/eliminar", methods=["POST"])
def eliminar_perfil():
    if not usuario_es_valido():
        return redirect(url_for("auth.login"))
    cookies = {BACKEND_SESSION_COOKIE_NAME: session.get(FRONTEND_COOKIE_CLAVE,"")}
    respuesta = eliminar_mi_perfil(cookies)

    if respuesta.get("message",""):
        session.clear()
        return redirect(url_for("auth.login"), 303)
    else:
        flash("Error al eliminar el perfil", "error")
        return redirect(url_for("usuarios.mi_perfil"))