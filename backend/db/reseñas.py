from db.config import (
    ejecutar_query_lectura,
    ejecutar_query_escritura
)


def obtener_usuario_por_email(email):
    query = """
        SELECT *
        FROM usuarios
        WHERE email = %s
    """

    resultado = ejecutar_query_lectura(
        query,
        (email,)
    )

    return resultado[0] if resultado else None


def reserva_puede_reseñarse(
    id_reserva,
    id_usuario
):
    query = """
        SELECT *
        FROM reserva_mesa rm
        INNER JOIN reserva r
            ON rm.id_reserva = r.id_reserva
        WHERE rm.id_reserva = %s
        AND r.id_usuario = %s
        AND rm.estado = 'finalizada'
        AND rm.reseñada = FALSE
    """

    resultado = ejecutar_query_lectura(
        query,
        (
            id_reserva,
            id_usuario
        )
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
            pendiente,
            aprobada
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            TRUE,
            FALSE
        )
    """

    return ejecutar_query_escritura(
        query,
        (
            id_usuario,
            id_reserva,
            calificacion,
            comentario
        )
    )


def marcar_reserva_reseñada(
    id_reserva
):
    query = """
        UPDATE reserva_mesa
        SET reseñada = TRUE
        WHERE id_reserva = %s
    """

    ejecutar_query_escritura(
        query,
        (id_reserva,)
    )


def obtener_reseñas_aprobadas():
    query = """
        SELECT
            r.id_reseña,
            r.id_reserva,
            r.fecha,
            r.calificacion,
            r.comentario,
            r.aprobada,
            r.pendiente,
            u.email
        FROM reseña r
        LEFT JOIN usuarios u
            ON r.id_usuario = u.id_usuario
        WHERE r.aprobada = TRUE
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
            r.aprobada,
            r.pendiente,
            u.email
        FROM reseña r
        LEFT JOIN usuarios u
            ON r.id_usuario = u.id_usuario
        ORDER BY r.fecha DESC
    """

    return ejecutar_query_lectura(query)