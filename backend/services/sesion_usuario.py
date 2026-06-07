from flask import session
from services.messages import error_msg
from werkzeug.security import generate_password_hash, check_password_hash

from db.sesion_usuario import (
    obtener_usuario_por_email,
    crear_usuario
)

def login_service(data):
    email = data.get("email")
    password = data.get("password")
    print(email, password)
    if not email or not password:
        return error_msg(
            400,
            "Falta email o contraseña",description="Uno de los 2 campos de email o contraseña no fue ingresado correctamente."
        )

    usuario = obtener_usuario_por_email(email)

    if not usuario:
        return error_msg(
            404,
            "El usuario no existe",description="No se encontró ningún usuario registrado con el email proporcionado."
        )
    is_password_correct = check_password_hash(usuario["password"], password)
    if not is_password_correct:
        return error_msg(
            401,
            "Contraseña incorrecta",description="La contraseña ingresada no coincide con la registrada para este email."
        )

    session["id_usuario"] = usuario["id_usuario"]
    session["email"] = usuario["email"]
    session["es_admin"] = usuario["es_admin"]

    return {"msg":"El usuario ha iniciado sesión correctamente."}, 201


def register_service(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error_msg(
            400,
            "Falta email o contraseña",description="Uno de los 2 campos de email o contraseña no fue ingresado correctamente."
        )

    usuario_existe = (obtener_usuario_por_email(email))

    if not usuario_existe:
        contraseña_hasheada = generate_password_hash(password)
        id_usuario = crear_usuario(email, contraseña_hasheada)

        session["id_usuario"] = id_usuario
        session["email"] = email
        session["es_admin"] = False

        return {"msg": "El usuario ha sido registrado e iniciado sesión correctamente."}, 201

    return error_msg(
        409,
        "El usuario ya existe",description="Ya existe un usuario registrado con el email proporcionado."
    )

def logout_service():
    try:
        session.pop("id_usuario")
    except:
        return error_msg(
            400,
            "No estas logueado",description="No se encontró una sesión activa para cerrar."
        )

    session.clear()

    return {"msg": "El usuario ha cerrado sesión correctamente."}, 201

