from db.reseñas import (
    obtener_usuario_por_email,
    reserva_puede_reseñarse,
    crear_reseña,
    marcar_reserva_reseñada,
    obtener_reseñas_aprobadas,
    obtener_todas_las_reseñas,
    modificar_estado_reseña
)

from services.messages import error_msg


def crear_reseña_service(data):
    email = data.get("email")
    password = data.get("password")

    id_reserva = data.get("id_reserva")
    calificacion = data.get("calificacion")
    comentario = data.get("comentario")

    if not email or not password:
        return error_msg(
            400,
            "Faltan credenciales"
        )

    usuario = obtener_usuario_por_email(
        email
    )

    if not usuario:
        return error_msg(
            404,
            "Usuario no encontrado"
        )

    if usuario["password"] != password:
        return error_msg(
            401,
            "Password incorrecta"
        )

    if not id_reserva:
        return error_msg(
            400,
            "Falta id_reserva"
        )

    if not calificacion:
        return error_msg(
            400,
            "Falta calificacion"
        )

    if calificacion < 1 or calificacion > 5:
        return error_msg(
            400,
            "Calificacion invalida",
            description="Debe estar entre 1 y 5"
        )

    if not reserva_puede_reseñarse(
        id_reserva,
        usuario["id_usuario"]
    ):
        return error_msg(
            400,
            "La reserva no puede reseñarse"
        )

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
        "message": "Reseña creada",
        "id_reseña": id_reseña
    }, 201


def obtener_reseñas_aprobadas_service():
    reseñas = obtener_reseñas_aprobadas()

    return {
        "data": reseñas
    }, 200


def obtener_todas_las_reseñas_service():
    reseñas = obtener_todas_las_reseñas()

    return {
        "data": reseñas
    }, 200


def modificar_reseña_service(
    id_reseña,
    data
):
    aprobada = data.get("aprobada")
    pendiente = data.get("pendiente")

    if (
        aprobada is None and
        pendiente is None
    ):
        return error_msg(
            400,
            "No hay campos para modificar"
        )

    modificada = modificar_estado_reseña(
        id_reseña,
        aprobada,
        pendiente
    )

    if not modificada:
        return error_msg(
            400,
            "No se pudo modificar la reseña"
        )

    return {
        "message": "Reseña modificada"
    }, 200