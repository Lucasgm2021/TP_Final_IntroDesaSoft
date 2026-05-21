from flask import session
from db.config import (
    ejecutar_query_lectura,
    ejecutar_query_escritura
)

def crear_cliente( email,contraseña): #usado por cliente
    #es_admin por defecto es False, el cliente no puede elegir ser admin y la cantidad de reservas y canceladas por default son 0
    query = """
        INSERT INTO usuarios (
            email,
            password
        )
        VALUES (:email,:contraseña) 
    """

    ejecutar_query_escritura(
        query,
        {
            "email": email,
            "contraseña": contraseña
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
        SELECT id_usuario, email, es_admin
        FROM usuarios
        WHERE email = :email
    """

    resultado = ejecutar_query_lectura(
        query,
        {"email": email.strip()}
    )

    if resultado:
        return dict(resultado[0]) #deberia haber solo un resultado, el email es unico
    else:       
        return None

def obtener_usuario_id(id_usuario):
    query = """
        SELECT id_usuario, email, es_admin
        FROM usuarios
        WHERE id_usuario = :id_usuario
    """

    resultado = ejecutar_query_lectura(
        query,
        {"id_usuario": id_usuario}
    )

    if resultado:
        return dict(resultado[0]) #deberia haber solo un resultado, el id es unico
    else:       
        return None

def actualizar_mi_perfil(id_usuario,nuevo_email,nueva_contraseña):#usado por cliente
    query = """
        UPDATE usuarios
        SET email = :email,
            password = :password
        WHERE id_usuario = :id_usuario
    """

    ejecutar_query_escritura(
        query,
        {
            "email": nuevo_email,
            "password": nueva_contraseña,
            "id_usuario": id_usuario #session["id_|usuario"]
        }
    )

def actualizar_usuario(email,es_admin):#usado por admins
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


def borrar_usuario(id_usuario):#usado por admin
    query = """
        DELETE FROM usuarios
        WHERE id_usuario = :id_usuario
    """

    ejecutar_query_escritura(query,{"id_usuario": id_usuario})