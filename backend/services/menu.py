from db.menu import (
    obtener_todos_los_platos,
    obtener_plato_por_id,
    crear_plato,
    modificar_plato,
    borrar_plato
)

from services.messages import error_msg


def obtener_menu_service():
    platos = obtener_todos_los_platos()
    platos = [dict(row) for row in platos]
    return {
        "data": platos
    }, 200


def obtener_plato_service(id_plato):
    plato = obtener_plato_por_id(id_plato)

    if not plato: #busca plato por ID y valida si existe
        return error_msg(
            404,
            "Plato no encontrado"
        )

    return {
        "data": plato
    }, 200


def crear_plato_service(data):

    #extrae los datos que mando el usuario del diccionario data que proviene de routes
    nombre = data.get("nombre")
    precio = data.get("precio")
    id_categoria = data.get("id_categoria")
    link_imagen = data.get("link_imagen")
    hay_stock = data.get("hay_stock")
    gluten = data.get("gluten")
    producto_animal = data.get("producto_animal")
    carnes = data.get("carnes")
    lactosa = data.get("lactosa")

    if not nombre:
        return error_msg(400, "Falta nombre del plato")

    if precio is None:
        return error_msg(400, "Falta precio del plato")

    if precio <= 0:
        return error_msg(
            400,
            "Precio invalido",
            description="El precio debe ser mayor a 0"
        )

    #guarda el plato nuevo en la bd porque se comprobo que el plato es valido
    id_plato = crear_plato(
        id_categoria, nombre, link_imagen, precio, hay_stock,
        gluten, producto_animal, carnes, lactosa
    )

    return {
        "message": "Plato creado exitosamente",
        "id_plato": id_plato
    }, 201


def modificar_plato_service(id_plato, data): #valida la existencia y el precio de un plato antes de actualizarlo en la bd

    plato_existente = obtener_plato_por_id(id_plato)
    if not plato_existente:
        return error_msg(404, "Plato no encontrado")

    precio = data.get("precio")
    if precio is not None and float(precio) <= 0:
        return error_msg(
            400,
            "Precio invalido",
            description="El precio debe ser mayor a 0"
        )

    #guarda los cambios del plato en la bd (por ej si aumenta el precio)
    modificar_plato(
        id_plato,
        data.get("id_categoria"),
        data.get("nombre"),
        data.get("link_imagen"),
        data.get("precio"),
        data.get("hay_stock"),
        data.get("gluten"),
        data.get("producto_animal"),
        data.get("carnes"),
        data.get("lactosa")
    )

    return {
        "message": "Plato modificado exitosamente"
    }, 200


def borrar_plato_service(id_plato):

    plato_existente = obtener_plato_por_id(id_plato)

    if not plato_existente: #verifica antes de llamar a borrar_plato
        return error_msg(404, "Plato no encontrado")

    borrar_plato(id_plato)

    return {
        "message": "Plato eliminado exitosamente"
    }, 200