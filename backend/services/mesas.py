from db.mesas import (
    obtener_mesas,
    obtener_mesas_validas,
    obtener_mesa_por_id,
    existe_numero_mesa,
    obtener_total_mesas,
    obtener_total_mesas_en_uso,
    crear_mesa,
    modificar_mesa,
    mesa_tiene_reservas_activas,
    eliminar_mesa
)

from services.messages import error_msg


def obtener_mesas_service():
    mesas = obtener_mesas()
    mesas = [dict(row) for row in mesas]

    return {"data": mesas}, 200

def obtener_mesas_validas_service(data):
    mesas = obtener_mesas_validas(data)
    mesas = [dict(row) for row in mesas]
    return {"data": mesas}, 200

def obtener_mesa_service(id_mesa):
    mesa = obtener_mesa_por_id(id_mesa)

    if not mesa:
        return error_msg(404, "Mesa no encontrada")

    return {"data": dict(mesa)}, 200

def obtener_mesas_disponibles():
    #total de mesas - mesas usadas en un determinado momento = mesas disponibles en ese momento
    total_mesas = obtener_total_mesas()
    mesas_en_uso = obtener_total_mesas_en_uso()

    mesas_disponibles = total_mesas - mesas_en_uso

    if mesas_disponibles < 0:
        mesas_disponibles = 0

    return {"mesas_disponibles":mesas_disponibles},200

def crear_mesa_service(data):
    numero = data.get("numero")
    capacidad = data.get("capacidad")
    interior = data.get("interior")
    funcional = data.get("funcional", True)

    if numero is None:
        return error_msg(400, "Falta numero")

    if capacidad is None:
        return error_msg(400, "Falta capacidad")

    if interior is None:
        return error_msg(400, "Falta interior")

    if not isinstance(numero, int) or numero <= 0:
        return error_msg(
            400,
            "Numero invalido",
            description="Debe ser un entero positivo"
        )

    if not isinstance(capacidad, int) or capacidad <= 0:
        return error_msg(
            400,
            "Capacidad invalida",
            description="Debe ser un entero positivo"
        )

    if existe_numero_mesa(numero):
        return error_msg(
            400,
            "Numero de mesa ya existe",
            description=f"Ya existe una mesa con el número {numero}"
        )

    id_mesa = crear_mesa(numero, capacidad, interior, funcional)

    return {"message": "Mesa creada", "id_mesa": id_mesa}, 201


def modificar_mesa_service(id_mesa, data):
    mesa = obtener_mesa_por_id(id_mesa)

    if not mesa:
        return error_msg(404, "Mesa no encontrada")

    campos_permitidos = ["numero", "capacidad", "interior", "funcional"]
    campos = {}

    for campo in campos_permitidos:
        if campo in data:
            campos[campo] = data[campo]

    if not campos:
        return error_msg(400, "No se enviaron campos a modificar")

    if "numero" in campos:
        numero = campos["numero"]
        if not isinstance(numero, int) or numero <= 0:
            return error_msg(
                400,
                "Numero invalido",
                description="Debe ser un entero positivo"
            )
        if existe_numero_mesa(numero, excluir_id=id_mesa):
            return error_msg(
                400,
                "Numero de mesa ya existe",
                description=f"Ya existe una mesa con el número {numero}"
            )

    if "capacidad" in campos:
        capacidad = campos["capacidad"]
        if not isinstance(capacidad, int) or capacidad <= 0:
            return error_msg(
                400,
                "Capacidad invalida",
                description="Debe ser un entero positivo"
            )

    modificar_mesa(id_mesa, campos)

    return {"message": "Mesa modificada"}, 200


def eliminar_mesa_service(id_mesa):
    mesa = obtener_mesa_por_id(id_mesa)

    if not mesa:
        return error_msg(404, "Mesa no encontrada")

    if mesa_tiene_reservas_activas(id_mesa):
        return error_msg(
            400,
            "No se puede eliminar la mesa",
            description="Tiene reservas pendientes asociadas"
        )

    eliminar_mesa(id_mesa)

    return {"message": "Mesa eliminada"}, 200