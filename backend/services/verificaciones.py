from services.messages import error_msg
from flask import session, request


def check_usuario():
    if "id_usuario" not in session:
        return False, error_msg(401, "Necesitas iniciar sesion",description="No se encontró una sesión activa. Por favor, inicia sesión para acceder a este recurso o realizar la acción.")

    return True, None

def check_usuario_es_admin():
    if not session.get("id_usuario"):
        return (
            False,
            error_msg(
                401,
                "Necesitas iniciar sesion como administrador",description="No se encontró una sesión activa. Por favor, inicia sesión con una cuenta de administrador para acceder a este recurso o realizar la acción."
            )
        )

    if not session.get("es_admin", False):
        return (
            False,
            error_msg(
                403,
                "Necesitas permisos de administrador",description="No tienes permisos suficientes para acceder a este recurso. Por favor, inicia sesión con una cuenta de administrador."
            )
        )

    return True, None