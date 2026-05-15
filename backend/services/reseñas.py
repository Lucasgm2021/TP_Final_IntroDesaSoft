from db.reseñas import (
    obtener_usuario_por_email,
    reserva_puede_reseñarse,
    crear_reseña,
    marcar_reserva_reseñada,
    obtener_reseñas_aprobadas,
    obtener_todas_las_reseñas
)


def crear_reseña_service(data):
    email = data.get("email")
    password = data.get("password")

    id_reserva = data.get("id_reserva")
    calificacion = data.get("calificacion")
    comentario = data.get("comentario")

    if not email or not password:
        return {
            "ok": False,
            "mensaje": "Faltan credenciales"
        }, 400

    usuario = obtener_usuario_por_email(
        email
    )

    if not usuario:
        return {
            "ok": False,
            "mensaje": "Usuario no encontrado"
        }, 404

    if usuario["password"] != password:
        return {
            "ok": False,
            "mensaje": "Password incorrecta"
        }, 401

    if not reserva_puede_reseñarse(
        id_reserva,
        usuario["id_usuario"]
    ):
        return {
            "ok": False,
            "mensaje": "La reserva no puede reseñarse"
        }, 400

    id_reseña = crear_reseña(
        usuario["id_usuario"],
        id_reserva,
        calificacion,
        comentario
    )

    marcar_reserva_reseñada(
        id_reserva
    )

    return {
        "ok": True,
        "mensaje": "Reseña creada",
        "id_reseña": id_reseña
    }, 201


def obtener_reseñas_aprobadas_service():
    reseñas = obtener_reseñas_aprobadas()

    return {
        "ok": True,
        "reseñas": reseñas
    }, 200


def obtener_todas_las_reseñas_service():
    reseñas = obtener_todas_las_reseñas()

    return {
        "ok": True,
        "reseñas": reseñas
    }, 200