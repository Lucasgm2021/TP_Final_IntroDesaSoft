from flask import session

from db.reseñas import (
    reserva_puede_reseñarse,
    crear_reseña,
    marcar_reserva_reseñada,
    obtener_reseñas_aprobadas,
    obtener_todas_las_reseñas,
    modificar_estado_reseña, obtener_todas_las_reseñables_usuario
)

from services.messages import error_msg


def crear_reseña_service(data):
    id_reserva = data.get("id_reserva") #Debería ser data que llegue por un formulario, con dropdown, de las reservas a las que se fue.
    calificacion = data.get("calificacion")
    comentario = data.get("comentario")

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
        id_reserva
    ):
        return error_msg(
            400,
            "La reserva no puede reseñarse"
        )

    id_reseña = crear_reseña(
        session["id_usuario"],
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
    reseñas = [dict(row) for row in reseñas]

    return {
        "data": reseñas
    }, 200


def obtener_todas_las_reseñas_service():
    reseñas = obtener_todas_las_reseñas()
    reseñas = [dict(row) for row in reseñas]
    return {
        "data": reseñas
    }, 200


def modificar_reseña_service(
    id_reseña,
    data
):
    estado = data.get("estado")

    estados_validos = [
        "no_aprobada",
        "aprobada"
    ]

    if not estado:
        return error_msg(
            400,
            "Falta estado"
        )

    if estado not in estados_validos:
        return error_msg(
            400,
            "Estado invalido",
            description="Estados validos: \"aprobada\", \"no_aprobada\""
        )

    modificada = modificar_estado_reseña(
        id_reseña,
        estado
    )

    if not modificada:
        return error_msg(
            400,
            "No se pudo modificar la reseña"
        )

    return error_msg(200, "Reseña modificada","comment")

def reservas_reseñables_service():
    reseñas = obtener_todas_las_reseñables_usuario()
    return [dict(row) for row in reseñas]