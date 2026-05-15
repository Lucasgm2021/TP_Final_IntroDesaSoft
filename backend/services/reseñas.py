from db.reseñas import (
    obtener_cliente_por_email,
    reserva_puede_reseñarse,
    crear_reseña,
    marcar_reserva_reseñada,
    obtener_reseñas_aprobadas,
    obtener_todas_las_reseñas
)

def crear_reseña_service(data):
    email = data.get("email")

    id_reserva = data.get("id_reserva")
    calificacion = data.get("calificacion")
    comentario = data.get("comentario")

    if not email:
        return {
            "ok": False,
            "mensaje": "Falta email"
        }, 400

    cliente = obtener_cliente_por_email(email)

    if not cliente:
        return {
            "ok": False,
            "mensaje": "Cliente no encontrado"
        }, 404

    if not reserva_puede_reseñarse(
        id_reserva,
        cliente["id_clientes"]
    ):
        return {
            "ok": False,
            "mensaje": (
                "La reserva no puede reseñarse"
            )
        }, 400

    id_reseña = crear_reseña(
        cliente["id_clientes"],
        id_reserva,
        calificacion,
        comentario
    )

    marcar_reserva_reseñada(id_reserva)

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