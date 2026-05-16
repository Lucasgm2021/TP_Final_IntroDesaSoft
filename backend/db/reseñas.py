from flask import session

from db.config import (
    ejecutar_query_lectura,
    ejecutar_query_escritura
)

def reserva_puede_reseñarse(
    id_reserva
):
    query = """
        SELECT *
        FROM reserva_mesa rm
        INNER JOIN reserva r
            ON rm.id_reserva = r.id_reserva
        WHERE rm.id_reserva = :id_reserva
        AND r.id_usuario = :id_usuario
        AND rm.estado = 'finalizada'
        AND rm.reseñada = FALSE
    """

    resultado = ejecutar_query_lectura(
        query,
        {
            "id_reserva":id_reserva,
            "id_usuario":session["id_usuario"],
        }
    )

    return len(resultado) > 0


def crear_reseña(
    id_usuario,
    id_reserva,
    calificacion,
    comentario
):
    query = """
        INSERT INTO reseña (
            id_usuario,
            id_reserva,
            calificacion,
            comentario,
            estado
        )
        VALUES (
            :id_usuario,
            :id_reserva,
            :calificacion,
            :comentario,
            'no_revisada'
        )
    """

    return ejecutar_query_escritura(
        query,
        {
            "id_usuario":session["id_usuario"],
            "id_reserva":id_reserva,
            "calificacion":calificacion,
            "comentario":comentario
        }
    )


def marcar_reserva_reseñada(
    id_reserva
):
    query = """
        UPDATE reserva_mesa
        SET reseñada = TRUE
        WHERE id_reserva = :id_reserva
    """

    ejecutar_query_escritura(
        query,
        {"id_reserva":id_reserva}
    )


def obtener_reseñas_aprobadas():
    query = """
        SELECT
            r.id_reseña,
            r.id_reserva,
            r.fecha,
            r.calificacion,
            r.comentario,
            r.estado,

            u.id_usuario,
            u.email

        FROM reseña r

        LEFT JOIN usuarios u
            ON r.id_usuario = u.id_usuario

        WHERE r.estado = 'aprobada'

        ORDER BY r.fecha DESC
    """

    return ejecutar_query_lectura(query)


def obtener_todas_las_reseñas():
    query = """
        SELECT
            r.id_reseña,
            r.id_reserva,
            r.fecha,
            r.calificacion,
            r.comentario,
            r.estado,

            u.id_usuario,
            u.email

        FROM reseña r

        LEFT JOIN usuarios u
            ON r.id_usuario = u.id_usuario

        ORDER BY r.fecha DESC
    """

    return ejecutar_query_lectura(query)


def modificar_estado_reseña(
    id_reseña,
    estado
):
    query = """
        UPDATE reseña
        SET estado = :estado
        WHERE id_reseña = :id_reseña
    """

    ejecutar_query_escritura(
        query,
        {
            "estado":estado,
            "id_reseña":id_reseña
        }
    )

    return True

def obtener_todas_las_reseñables_usuario():
    query = """
        SELECT r.id_reseña FROM reseña r
        LEFT JOIN usuarios u ON r.id_usuario = u.id_usuario
        WHERE u.id_usuario = :id_usuario
    """

    return ejecutar_query_lectura(query,{"id_usuario":session["id_usuario"]})