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
        WHERE id_plato = :id_plato
    """
    resultado = ejecutar_query_lectura(query, {"id_plato": id_plato})
    return dict(resultado[0]) if resultado else None

def crear_plato(id_categoria, nombre, link_imagen, precio, hay_stock, gluten, producto_animal, carnes, lactosa): #admin: inserta un plato nuevo
    query = """
        INSERT INTO plato (id_categoria, nombre, link_imagen, precio, hay_stock, gluten, producto_animal, carnes, lactosa)
        VALUES (:id_categoria, :nombre, :link_imagen, :precio, :hay_stock, :gluten, :producto_animal, :carnes, :lactosa)
    """
    return ejecutar_query_escritura(query, {
        "id_categoria": id_categoria,
        "nombre": nombre,
        "link_imagen": link_imagen,
        "precio": precio,
        "hay_stock": hay_stock,
        "gluten": gluten,
        "producto_animal": producto_animal,
        "carnes": carnes,
        "lactosa": lactosa
    })

def modificar_plato(id_plato, id_categoria, nombre, link_imagen, precio, hay_stock, gluten, producto_animal, carnes, lactosa): #admin: cambia los datos
    query = """
        UPDATE plato
        SET id_categoria = :id_categoria, nombre = :nombre, link_imagen = :link_imagen, precio = :precio, hay_stock = :hay_stock, 
            gluten = :gluten, producto_animal = :producto_animal, carnes = :carnes, lactosa = :lactosa
        WHERE id_plato = :id_plato
    """
    ejecutar_query_escritura(query, {
        "id_categoria": id_categoria,
        "nombre": nombre,
        "link_imagen": link_imagen,
        "precio": precio,
        "hay_stock": hay_stock,
        "gluten": gluten,
        "producto_animal": producto_animal,
        "carnes": carnes,
        "lactosa": lactosa,
        "id_plato": id_plato
    })
    return True

def borrar_plato(id_plato): #admin: borra un plato definitivamente
    query = """
        DELETE FROM plato
        WHERE id_plato = :id_plato
    """
    ejecutar_query_escritura(query, {"id_plato": id_plato})
    return True