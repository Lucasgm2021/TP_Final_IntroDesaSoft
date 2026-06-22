from flask import session
from db.config import (
    ejecutar_query_lectura,
    ejecutar_query_escritura
)

def crear_cliente( email,contraseña): #usado por cliente
    query = """
        INSERT INTO usuarios (
            email,
            password
        )
        VALUES (:email,:password) 
    """

    ejecutar_query_escritura(
        query,
        {
            "email": email,
            "password": contraseña
        }
    )

def crear_usuario( email,contraseña,es_admin): #usado por admin
    query = """
        INSERT INTO usuarios (
            email,
            password,
            es_admin
        )
        VALUES (:email,:password,:es_admin)
    """

    ejecutar_query_escritura(
        query,
        {
            "email": email,
            "password": contraseña,
            "es_admin": es_admin
        }
    )


def obtener_usuarios():
    query = """
        SELECT id_usuario, email, es_admin
        FROM usuarios
    """

    return ejecutar_query_lectura(query)


def obtener_usuario_email(email):
    query = """
        SELECT id_usuario, email, es_admin, password
        FROM usuarios
        WHERE email = :email
    """

    resultado = ejecutar_query_lectura(
        query,
        {"email": email.strip()}
    )

    if resultado:
        return dict(resultado[0]) 
    else:       
        return None

def obtener_usuario_id(id_usuario):
    query = """
        SELECT id_usuario, email, es_admin, password
        FROM usuarios
        WHERE id_usuario = :id_usuario
    """

    resultado = ejecutar_query_lectura(
        query,
        {"id_usuario": id_usuario}
    )

    if resultado:
        return dict(resultado[0]) 
    else:       
        return None

def actualizar_mi_perfil(id_usuario,data_a_modificar):
    setters = ", ".join([f"{campo}=:{campo}" for campo in data_a_modificar])
    query = f"""
        UPDATE usuarios
        SET {setters}
        WHERE id_usuario = :id_usuario
    """

    data_a_modificar["id_usuario"] = id_usuario

    ejecutar_query_escritura(query,data_a_modificar)

def actualizar_usuario(email,es_admin):
    query = """
        UPDATE usuarios
        SET es_admin = :es_admin
        WHERE email = :email
    """

    ejecutar_query_escritura(
        query,
        {
            "es_admin": es_admin,
            "email": email
        }
    )


def borrar_usuario(id_usuario):
    query = """
        DELETE FROM usuarios
        WHERE id_usuario = :id_usuario
    """

    ejecutar_query_escritura(query,{"id_usuario": id_usuario})