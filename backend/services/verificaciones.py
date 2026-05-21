from services.messages import error_msg
from flask import session, request


def check_usuario():
    if "id_usuario" not in session:
        return False, error_msg(401, "Necesitas iniciar sesion como usuario")

    return True, None

def check_usuario_es_admin():
    if not session.get("id_usuario"):
        return (
            False,
            error_msg(
                401,
                "Necesitas iniciar sesion"
            )
        )

    if not session.get("es_admin", False):
        return (
            False,
            error_msg(
                403,
                "Necesitas permisos de administrador"
            )
        )

    return True, None