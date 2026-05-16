import db.reservas as queries_reservas
import services.mail as mail

def obtener_reservas(offset,limit):
    return queries_reservas.obtener_reservas(offset,limit)

def contar_total_reservas():
    return list(queries_reservas.obtener_total_reservas()[0].values())[0]

def crear_reserva():
    mail.enviar_mail_con_qr()