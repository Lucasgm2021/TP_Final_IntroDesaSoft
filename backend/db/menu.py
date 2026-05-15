from db.config import ejecutar_query_lectura, ejecutar_query_escritura

def obtener_todos_los_platos(): #clientes: obtiene todos los platos del menú
    query = """
        SELECT id_plato, id_categoria, nombre, link_imagen, precio, hay_stock, gluten, producto_animal, carnes, lactosa
        FROM plato
    """
    return ejecutar_query_lectura(query)

def obtener_plato_por_id(id_plato): #busca un solo plato especifico por ID
    query = """
        SELECT id_plato, id_categoria, nombre, link_imagen, precio, hay_stock, gluten, producto_animal, carnes, lactosa
        FROM plato
        WHERE id_plato = %s
    """
    resultado = ejecutar_query_lectura(query, (id_plato,))
    return resultado[0] if resultado else None

def crear_plato(id_categoria, nombre, link_imagen, precio, hay_stock, gluten, producto_animal, carnes, lactosa): # admin: inserta un plato nuevo en la base de datos
    query = """
        INSERT INTO plato (id_categoria, nombre, link_imagen, precio, hay_stock, gluten, producto_animal, carnes, lactosa)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    return ejecutar_query_escritura(query, (id_categoria, nombre, link_imagen, precio, hay_stock, gluten, producto_animal, carnes, lactosa))

def modificar_plato(id_plato, id_categoria, nombre, link_imagen, precio, hay_stock, gluten, producto_animal, carnes, lactosa):
#admin: cambia los datos o el stock de un plato que ya existe
    query = """
        UPDATE plato
        SET id_categoria = %s, nombre = %s, link_imagen = %s, precio = %s, hay_stock = %s, 
            gluten = %s, producto_animal = %s, carnes = %s, lactosa = %s
        WHERE id_plato = %s
    """
    ejecutar_query_escritura(query, (id_categoria, nombre, link_imagen, precio, hay_stock, gluten, producto_animal, carnes, lactosa, id_plato))
    return True

def borrar_plato(id_plato): #admin: borra un plato de la lista definitivamente
    query = """
        DELETE FROM plato
        WHERE id_plato = %s
    """
    ejecutar_query_escritura(query, (id_plato,))
    return True