from db.config import (
    ejecutar_query_lectura,
    ejecutar_query_escritura
)

def crear_configuracion( clave,valor ):
    query = """
        INSERT INTO configuracion (
            clave,
            valor
        )
        VALUES (:clave,:valor)
    """

    ejecutar_query_escritura(
        query,
        {
            "clave": clave,
            "valor": valor
        }
    )


def obtener_toda_la_configuracion():
    query = """
        SELECT clave, valor
        FROM configuracion
    """

    return ejecutar_query_lectura(query)


def obtener_configuracion_por_clave(
    clave
):
    query = """
        SELECT clave, valor
        FROM configuracion
        WHERE clave = :clave
    """

    resultado = ejecutar_query_lectura(
        query,
        {"clave": clave}
    )

    return resultado[0] if resultado else None


def actualizar_configuracion(
    clave,
    valor
):
    query = """
        UPDATE configuracion
        SET valor = :valor
        WHERE clave = :clave
    """

    ejecutar_query_escritura(
        query,
        {
            "valor": valor,
            "clave": clave
        }
    )


def borrar_configuracion(
    clave
):
    query = """
        DELETE FROM configuracion
        WHERE clave = :clave
    """

    ejecutar_query_escritura(
        query,
        {"clave": clave}
    )