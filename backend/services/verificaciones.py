from flask import session, redirect

from services.messages import error_msg

def check_usuario_es_admin():

    if "es_admin" not in session:
        return (
            False,
            error_msg(
                401,
                "Necesitas iniciar sesion como administrador"
            )
        )

    if not session["es_admin"]:
        return (
            False,
            error_msg(
                403,
                "Necesitas permisos de administrador"
            )
        )

    return (
        True,
        None
    )

def check_usuario():
    if "id_usuario" not in session:
        return False, error_msg(401, "Necesitas iniciar sesion como usuario")
    return True, None