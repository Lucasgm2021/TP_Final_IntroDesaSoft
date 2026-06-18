from flask import session

from db.config import (
    ejecutar_query_lectura,
    ejecutar_query_escritura
)


def reserva_puede_reseñarse(id_reserva):
    query = """
        SELECT
            r.id_reserva
        FROM reserva r

        LEFT JOIN resenia re
            ON r.id_reserva = re.id_reserva

        WHERE
            r.id_reserva = :id_reserva
            AND r.id_usuario = :id_usuario
            AND r.estado_reserva = 'finalizada'
            AND r.reseniada = FALSE
            AND r.fecha <= CURRENT_DATE
            AND re.id_resenia IS NULL
    """

    resultado = ejecutar_query_lectura(
        query,
        {
            "id_reserva": id_reserva,
            "id_usuario": session["id_usuario"],
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
        INSERT INTO resenia (
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
            "id_usuario": session["id_usuario"],
            "id_reserva": id_reserva,
            "calificacion": calificacion,
            "comentario": comentario
        }
    )


def marcar_reserva_reseñada(
    id_reserva
):
    query = """
        UPDATE reserva
        SET reseniada = TRUE
        WHERE id_reserva = :id_reserva
    """

    ejecutar_query_escritura(
        query,
        {
            "id_reserva": id_reserva
        }
    )


def obtener_reseñas_aprobadas():
    query = """
        SELECT
            re.id_resenia,
            re.id_reserva,
            re.fecha,
            re.calificacion,
            re.comentario,
            re.estado,

            u.id_usuario,
            u.email

        FROM resenia re

        LEFT JOIN usuarios u
            ON re.id_usuario = u.id_usuario

        WHERE re.estado = 'aprobada'

        ORDER BY re.fecha DESC
    """

    return ejecutar_query_lectura(query)


def obtener_todas_las_reseñas():
    query = """
        SELECT
            re.id_resenia,
            re.id_reserva,
            re.fecha,
            re.calificacion,
            re.comentario,
            re.estado,

            u.id_usuario,
            u.email

        FROM resenia re

        LEFT JOIN usuarios u
            ON re.id_usuario = u.id_usuario

        ORDER BY re.fecha DESC
    """

    return ejecutar_query_lectura(query)


def modificar_estado_reseña(
    id_resenia,
    estado
):
    query = """
        UPDATE resenia
        SET estado = :estado
        WHERE id_resenia = :id_resenia
    """

    ejecutar_query_escritura(
        query,
        {
            "estado": estado,
            "id_resenia": id_resenia
        }
    )

    return True



def obtener_todas_las_reseñables_usuario():
    query = """
        SELECT
            r.id_reserva,
            r.fecha,
            r.hora_reserva,
            r.comensales,
            r.interior

        FROM reserva r
        SELECT
            r.id_reserva,
            r.fecha,
            r.hora_reserva,
            r.comensales,
            r.interior

        FROM reserva r

        LEFT JOIN resenia re
            ON r.id_reserva = re.id_reserva

        WHERE
            r.id_usuario = :id_usuario
            AND r.estado_reserva = 'finalizada'
            AND r.reseniada = FALSE
            AND r.fecha <= CURRENT_DATE
            AND re.id_resenia IS NULL

        ORDER BY r.fecha DESC
    """

    return ejecutar_query_lectura(
        query,
        {
            "id_usuario": session["id_usuario"]
        }
    )

def obtener_mis_reseñas_query(id_usuario):
    query = """
        SELECT
            re.id_resenia,
            re.id_reserva,
            re.fecha,
            re.calificacion,
            re.comentario,
            re.estado,

            u.id_usuario,
            u.email

        FROM resenia re

        LEFT JOIN usuarios u
            ON re.id_usuario = u.id_usuario
        WHERE re.id_usuario = :id_usuario
        ORDER BY re.fecha DESC
    """
    return ejecutar_query_lectura(query,params={"id_usuario": id_usuario})