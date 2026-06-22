from db.config import (
    ejecutar_query_lectura,
    ejecutar_query_escritura
)


def obtener_mesas():

    query = f"""
        SELECT
            id_mesa,
            numero,
            capacidad,
            interior,
            funcional
        FROM mesa
        ORDER BY numero
    """

    return ejecutar_query_lectura(query)

def obtener_mesas_validas(data):
    query = f"""
        SELECT
            id_mesa,
            numero,
            capacidad
        FROM mesa
        WHERE mesa.id_mesa NOT IN (
            SELECT id_mesa
            FROM reserva_mesa
            JOIN reserva on reserva_mesa.id_reserva = reserva.id_reserva
            WHERE reserva.fecha = :fecha
            AND reserva.hora_reserva = :hora_reserva
            AND reserva.estado_reserva IN ('pendiente')
            AND reserva.interior = :interior
        ) AND funcional = true AND interior = :interior
    """

    return ejecutar_query_lectura(query,params={"fecha": data["fecha"], "hora_reserva": data["hora_reserva"], "interior": data["interior"]})


def obtener_mesa_por_id(id_mesa):
    query = """
        SELECT
            id_mesa,
            numero,
            capacidad,
            interior,
            funcional
        FROM mesa
        WHERE id_mesa = :id_mesa
    """

    resultado = ejecutar_query_lectura(query, {"id_mesa": id_mesa})
    return resultado[0] if resultado else None


def existe_numero_mesa(numero, excluir_id=None):
    if excluir_id:
        query = """
            SELECT id_mesa FROM mesa
            WHERE numero = :numero AND id_mesa != :excluir_id
        """
        params = {"numero": numero, "excluir_id": excluir_id}
    else:
        query = """
            SELECT id_mesa FROM mesa
            WHERE numero = :numero
        """
        params = {"numero": numero}

    resultado = ejecutar_query_lectura(query, params)
    return len(resultado) > 0


def obtener_total_mesas():
    query = " SELECT COUNT(*) as total FROM mesa"

    resultado = ejecutar_query_lectura(
        query
    )

    return resultado[0]["total"]

def obtener_total_mesas_en_uso():
    query = """
    SELECT COUNT(mesa.id_mesa) as total
    FROM mesa
    JOIN reserva_mesa ON reserva_mesa.id_mesa = mesa.id_mesa
    JOIN reserva ON reserva_mesa.id_reserva = reserva.id_reserva
    WHERE reserva.fecha = CURRENT_DATE()
    AND reserva.hora_reserva = CONCAT(HOUR(NOW()), ':00:00')
    AND reserva.estado_reserva IN ('pendiente')
    """
    resultado = ejecutar_query_lectura(query)
    return resultado[0]["total"]

def crear_mesa(numero, capacidad, interior, funcional):
    query = """
        INSERT INTO mesa (numero, capacidad, interior, funcional)
        VALUES (:numero, :capacidad, :interior, :funcional)
    """

    return ejecutar_query_escritura(
        query,
        {
            "numero": numero,
            "capacidad": capacidad,
            "interior": interior,
            "funcional": funcional
        }
    )


def modificar_mesa(id_mesa, campos):
    if not campos:
        return False

    setters = ", ".join(f"{campo} = :{campo}" for campo in campos)

    query = f"""
        UPDATE mesa
        SET {setters}
        WHERE id_mesa = :id_mesa
    """

    campos["id_mesa"] = id_mesa
    ejecutar_query_escritura(query, campos)
    return True


def mesa_tiene_reservas_activas(id_mesa):
    query = """
        SELECT r.id_reserva
        FROM reserva_mesa rm
        JOIN reserva r ON r.id_reserva = rm.id_reserva
        WHERE rm.id_mesa = :id_mesa
        AND r.estado_reserva = 'pendiente'
    """

    resultado = ejecutar_query_lectura(query, {"id_mesa": id_mesa})
    return len(resultado) > 0


def eliminar_mesa(id_mesa):
    query = """
        DELETE FROM mesa
        WHERE id_mesa = :id_mesa
    """

    ejecutar_query_escritura(query, {"id_mesa": id_mesa})
    return True