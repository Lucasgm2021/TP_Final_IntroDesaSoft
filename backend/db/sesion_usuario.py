from db.config import (
    ejecutar_query_lectura,
    ejecutar_query_escritura
)

def obtener_usuario_por_email(email):
    query = "SELECT * FROM usuarios WHERE email = :email"
    resultado = ejecutar_query_lectura(query, {"email": email})

    return resultado[0] if resultado else None

def crear_usuario(email,password):
    query = """
    INSERT INTO usuarios (email, password, es_admin) 
        VALUES (:email, :password, :es_admin)
    """

    return ejecutar_query_escritura(query, {
        "email":email,
        "password":password,
        "es_admin": False
    })
