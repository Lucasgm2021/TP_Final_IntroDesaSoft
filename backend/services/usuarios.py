from flask import session
import re
from db.usuarios import (
    crear_cliente,
    crear_usuario,
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

    crear_cliente(email,contraseña)

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

    crear_usuario(email,contraseña,es_admin)

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
    
    datos = {}
    for usuario in usuarios:
        datos[usuario["email"]] = {
            "id_usuario": usuario["id_usuario"],
            "es_admin": usuario["es_admin"]
        }

    return datos, 200

def obtener_usuario_email_service(email):
    if not validar_email(email):
        return error_msg(400, "Email no válido")
    
    usuario = obtener_usuario_email(email)
    if not usuario:
        return error_msg(404, "Usuario no encontrado")
    return usuario, 200

def actualizar_mi_perfil_service(data):
    for campo in ["nuevo_email", "nueva_contraseña"]:
        if campo not in data:
            return error_msg(400, f"Falta {campo}")

    nuevo_email = data["nuevo_email"]
    nueva_contraseña = data["nueva_contraseña"]
    #el formulario del front tiene como default el email actual (igual la contraseña), si el email no se cambia, no hace falta validar ni verificar que ya existe
    if nuevo_email != session["email"]: 
        if not validar_email(nuevo_email):
            return error_msg(400, "Email no válido")
        if obtener_usuario_email(nuevo_email) :
            return error_msg(409, "Ya hay un usuario registrado con ese email")

    actualizar_mi_perfil(session["id_usuario"],nuevo_email,nueva_contraseña)

    return {
        "message": (
            "Perfil actualizado"
        ),
        "data": {
            "nuevo_email": nuevo_email
        }
    }, 200

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

def validar_email(email):
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z]+\.[a-zA-Z]+$"
    return bool(re.match(patron, email))