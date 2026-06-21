from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
import re
from db.usuarios import (
    crear_cliente,
    crear_usuario,
    obtener_usuario_id,
    obtener_usuarios,
    obtener_usuario_email,
    actualizar_mi_perfil,
    actualizar_usuario,
    borrar_usuario
)

from services.messages import (error_msg)

def crear_cliente_service(data):

    for campo in ["email", "contraseña"]:
        if campo not in data:
            return error_msg(400, f"Falta {campo}")

    email = data["email"]
    contraseña = data["contraseña"]

    if not validar_email(email):
        return error_msg(400, "Email no válido")
    if obtener_usuario_email(email):
        return error_msg(409, "El email ya está registrado")

    contraseña_hasheada = generate_password_hash(contraseña)
    crear_cliente(email,contraseña_hasheada)

    return {
        "message": (
            "Cliente creado"
        ),
        "data": {
            "email": email
        }
    }, 201

def crear_usuario_service(data):

    for campo in ["email", "contraseña", "es_admin"]:
        if campo not in data:
            return error_msg(400, f"Falta {campo}")

    email = data["email"]
    contraseña = data["contraseña"]
    es_admin = data["es_admin"]

    if not validar_email(email):
        return error_msg(400, "Email no válido")
    if obtener_usuario_email(email):
        return error_msg(409, "El email ya está registrado")

    contraseña_hasheada = generate_password_hash(contraseña)
    crear_usuario(email,contraseña_hasheada,es_admin)

    return {
        "message": (
            "Usuario creado"
        ),
        "data": {
            "email": email,
            "es_admin": es_admin
        }
    }, 201

def obtener_usuarios_service():
    usuarios = obtener_usuarios()
    if not usuarios:
        return error_msg(404, "No hay usuarios registrados")

    usuarios = [dict(row) for row in usuarios]
    return {
        "data": usuarios
    }, 200

def obtener_usuario_email_service(email):
    if not validar_email(email):
        return error_msg(400, "Email no válido")
    
    usuario = obtener_usuario_email(email)
    if not usuario:
        return error_msg(404, "Usuario no encontrado")
    return usuario, 200

def obtener_mi_perfil_service():

    if "id_usuario" not in session:
        return error_msg(401, "No hay sesión activa")

    usuario = obtener_usuario_id(session["id_usuario"])
    if not usuario:
        return error_msg(404, "Usuario no encontrado")
    return usuario, 200

def actualizar_mi_perfil_service(data):

    if "id_usuario" not in session:
        return error_msg(401, "No hay sesión activa")

    nuevo_email = data["nuevo_email"]
    data_a_modificar = {}
    contraseña = data["nueva_contraseña"]

    if contraseña:
        try:
            contraseña_actual = obtener_usuario_email(session["email"])["password"]
        except:
            return error_msg(500, "Error al obtener el usuario actual")

        es_misma_contraseña = check_password_hash(contraseña_actual, contraseña)
        if not es_misma_contraseña:
            data_a_modificar["password"] = generate_password_hash(contraseña)

    if nuevo_email != session["email"]:
        if not validar_email(nuevo_email):
            return error_msg(400, "Email no válido")
        if obtener_usuario_email(nuevo_email) :
            return error_msg(409, "Ya hay un usuario registrado con ese email")
        data_a_modificar["email"] = nuevo_email

    if data_a_modificar:
        try:
            actualizar_mi_perfil(session["id_usuario"],data_a_modificar)
            session["email"] = nuevo_email
        except:
            return error_msg(500, "Error al actualizar el perfil")
        return {
            "message": (
                "Perfil actualizado"
            ),
            "data": {
                "nuevo_email": nuevo_email
            }
        }, 200
    else:
        return {
            "message": ("No hay datos por actualizar.")
        },200

def actualizar_usuario_service(data): #no puede cambiar su email ni contraseña
    for campo in ["email", "es_admin"]:
        if campo not in data:
            return error_msg(400, f"Falta {campo}")

    email = data["email"]
    nuevo_es_admin = data["es_admin"]

    actualizar_usuario(email,nuevo_es_admin)

    return {
        "message": (
            "Usuario actualizado"
        ),
        "data": {
            "email": email,
            "es_admin": nuevo_es_admin
        }
    }, 200

def eliminar_usuario_service(email):
    if not validar_email(email):
        return error_msg(400, "Email no válido")
    
    usuario = obtener_usuario_email(email)
    if not usuario:
        return error_msg(404, "Usuario no encontrado")

    borrar_usuario(usuario["id_usuario"])

    return {
        "message": (
            "Usuario eliminado"
        ),
        "data": {
            "email": email
        }
    }, 200

def eliminar_mi_perfil_service():
    if "id_usuario" not in session:
        return error_msg(401, "No hay sesión activa")

    usuario = obtener_usuario_id(session["id_usuario"])
    if not usuario:
        return error_msg(404, "Usuario no encontrado")

    borrar_usuario(usuario["id_usuario"])
    session.clear()

    return {
        "message": (
            "Perfil eliminado"
        )
    }, 200

def validar_email(email):
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z]+\.[a-zA-Z]+$"
    return bool(re.match(patron, email))