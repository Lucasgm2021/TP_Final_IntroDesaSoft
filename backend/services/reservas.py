import db.reservas as queries_reservas

def obtener_reservas(offset,limit):
    return queries_reservas.obtener_reservas(offset,limit)

def contar_total_reservas():
    return list(queries_reservas.obtener_total_reservas()[0].values())[0]
