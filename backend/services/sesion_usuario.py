from flask import session
from services.messages import error_msg

from db.sesion_usuario import (
    obtener_usuario_por_email,
    crear_usuario
)

def login_service(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error_msg(
            400,
            "Falta email o contraseña"
        )

    usuario = obtener_usuario_por_email(email)

    if not usuario:
        return error_msg(
            404,
            "El usuario no existe"
        )
    if usuario["password"] != password:
        return error_msg(
            401,
            "Contraseña incorrecta"
        )

    session["id_usuario"] = usuario["id_usuario"]
    session["email"] = usuario["email"]
    session["es_admin"] = usuario["es_admin"]

    return error_msg(
        200,
        "Logueado con exito",
        "confirmacion"

    )


def register_service(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error_msg(
            400,
            "Falta email o contraseña"
        )

    usuario_existe = (obtener_usuario_por_email(email))

    if not usuario_existe:
        id_usuario = crear_usuario(email, password)

        session["id_usuario"] = id_usuario
        session["email"] = email
        session["es_admin"] = False

        return error_msg(
            201,
            "Registrado con exito, sea iniciado sesion automaticamente",
            "confirmacion"
        )


    return error_msg(
        409,
        "El usuario ya existe"
    )

def logout_service():
    try:
        session.pop("id_usuario")
    except:
        return error_msg(
            400,
            "No estas logueado"
        )

    session.clear()

    return error_msg(
        200,
        "Deslogueado con exito",
        "confirmacion"
    )

