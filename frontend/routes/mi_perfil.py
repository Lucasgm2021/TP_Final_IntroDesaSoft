from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from servicesfront.mi_perfil import eliminar_mi_perfil, obtener_mi_perfil, actualizar_mi_perfil
from servicesfront.verificaciones import usuario_es_valido

usuarios_bp = Blueprint(
    "usuarios",
    __name__
)

@usuarios_bp.route("/cliente/mi_perfil", methods=["GET", "POST"])
def mi_perfil():

    if not usuario_es_valido():
        return redirect(url_for("auth_front.login"))
    usuario = obtener_mi_perfil()

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        status, response = actualizar_mi_perfil(email, password)

        if status == 200:
            flash("Perfil actualizado correctamente", "success")
            return redirect(url_for("usuarios.mi_perfil"))
        else:
            flash(response.get("error", "Error al actualizar"), "error")

    return render_template("mi_perfil.html",usuario=usuario)

@usuarios_bp.route("/cliente/mi_perfil/eliminar", methods=["POST"])
def eliminar_perfil():
    status = eliminar_mi_perfil()

    if status == 200:
        session.clear()
        return redirect(url_for("auth_front.login"), 303)
    else:
        flash("Error al eliminar el perfil", "error")
        return redirect(url_for("usuarios.mi_perfil"))