import db.reservas as queries_reservas
import services.mail as servicios_mail
from pathlib import Path

def obtener_reservas(offset,limit):
    return queries_reservas.obtener_reservas(offset,limit)

def contar_total_reservas():
    return list(queries_reservas.obtener_total_reservas()[0].values())[0]

def crear_reserva():

    mail_usuario = "lmino@fi.uba.ar"
    mail_template = Path(__file__).resolve().parent / "mail_reserva.html"
    asunto = "RESERVA REGISTRADA"
    datos_mail = {
        "qr_data": "http://localhost:5000/reservas/",
        "url_cancelar": "http://localhost:5000/reservas/cancelar"
    }

    servicios_mail.enviar_mail_con_qr(mail_usuario,asunto,datos_mail,mail_template)
    return "Todo ok",200