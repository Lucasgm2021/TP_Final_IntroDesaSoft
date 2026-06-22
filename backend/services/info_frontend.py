from db.info_frontend import (
    crear_configuracion,
    obtener_toda_la_configuracion,
    obtener_configuracion_por_clave,
    actualizar_configuracion,
    borrar_configuracion
)

from services.messages import (
    error_msg
)

def crear_info_service(data):
    clave = data.get("clave")
    valor = data.get("valor")

    if not clave:
        return error_msg(400,"Falta clave")
    if valor is None:
        return error_msg(400,"Falta valor")

    existente = (
        obtener_configuracion_por_clave(
            clave
        )
    )

    if existente:
        return error_msg(
            409,
            "La configuracion ya existe"
        )

    crear_configuracion(
        clave,
        valor
    )

    return {
        "message": (
            "Configuracion creada"
        ),
        "data": {
            clave: valor
        }
    }, 201


def obtener_info_service():
    configuraciones = (
        obtener_toda_la_configuracion()
    )

    config = [dict(row) for row in configuraciones]
    return {
        "data": config
    }, 200

def obtener_info_por_clave_service(
    clave
):
    configuracion = (
        obtener_configuracion_por_clave(
            clave
        )
    )

    if not configuracion:
        return error_msg(
            404,
            "Configuracion no encontrada"
        )

    return {
        configuracion["clave"]:
            configuracion["valor"]
    }, 200


def actualizar_info_service(
    clave,
    data
):
    valor = data.get("valor")

    if valor is None:
        return error_msg(
            400,
            "Falta valor"
        )

    configuracion = (
        obtener_configuracion_por_clave(
            clave
        )
    )

    if not configuracion:
        return error_msg(
            404,
            "Configuracion no encontrada"
        )

    actualizar_configuracion(
        clave,
        valor
    )

    return {
        "message": (
            "Configuracion actualizada"
        )
    }, 200


def borrar_info_service(
    clave
):
    configuracion = (
        obtener_configuracion_por_clave(
            clave
        )
    )

    if not configuracion:
        return error_msg(
            404,
            "Configuracion no encontrada"
        )

    borrar_configuracion(clave)

    return {
        "message": (
            "Configuracion eliminada"
        )
    }, 200