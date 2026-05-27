from flask import session

def usuario_es_admin():

    return (
        session.get("id_usuario") is not None
        and
        session.get("es_admin") is True
    )