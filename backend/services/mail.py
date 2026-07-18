import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage 
from email.mime.multipart import MIMEMultipart
import services.qr as qr
from constants import SERVIDOR_MAIL,PUERTO_MAIL,CUENTA_MAIL_LOGIN,CONTRASENA_MAIL,CUENTA_MAIL_FROM,SERVICIO_MAIL_GMAIL_APP_PASS,SERVICIO_MAIL_MAILJET

PROVEEDORES_CONFIG = {
    SERVICIO_MAIL_GMAIL_APP_PASS: {
        "server": SERVIDOR_MAIL,
        "port": PUERTO_MAIL, #465
        "from": CUENTA_MAIL_LOGIN,
        "user": CUENTA_MAIL_LOGIN,
        "password": CONTRASENA_MAIL,
        "use_ssl": True
    },
    SERVICIO_MAIL_MAILJET: {
        "server": SERVIDOR_MAIL,
        "port": PUERTO_MAIL, #2525
        "from": CUENTA_MAIL_FROM,
        "user": CUENTA_MAIL_LOGIN,#api key       
        "password": CONTRASENA_MAIL,#secret key  
        "use_ssl": False
    }
}

def construir_mensaje_con_qr(mail_from, mail_destino, asunto, mail_data, ruta_template):
    """
    Función interna (helper) encargada ÚNICAMENTE de construir el objeto MIMEMultipart.
    No sabe nada de servidores, puertos ni redes.
    """
    msg = MIMEMultipart("related")
    msg["From"] = mail_from
    msg["To"] = mail_destino
    msg["Subject"] = asunto

    if "qr_cid" not in mail_data:
        mail_data["qr_cid"] = "unique_id"

    with open(ruta_template, "r", encoding="utf-8") as file:
        raw_html_template = file.read()
    final_html_body = raw_html_template.format(**mail_data)

    msg_alternative = MIMEMultipart("alternative")
    msg_alternative.attach(MIMEText(final_html_body, "html"))
    msg.attach(msg_alternative)

    qr_bytes = qr.generate_qr_bytes(mail_data["qr_data"])
    image_mime = MIMEImage(qr_bytes, _subtype="png")
    image_mime.add_header("Content-ID", f"<{mail_data['qr_cid']}>")
    image_mime.add_header("Content-Disposition", "inline", filename="qrcode.png")
    msg.attach(image_mime)

    return msg

def enviar_mail_con_qr(proveedor, mail_destino, asunto, mail_data, ruta_template):
    if proveedor not in PROVEEDORES_CONFIG:
        raise ValueError(f"Proveedor '{proveedor}' no soportado.")
    
    config = PROVEEDORES_CONFIG[proveedor]
    
    msg = construir_mensaje_con_qr(config["from"], mail_destino, asunto, mail_data, ruta_template)
    try:
        if config["use_ssl"]:
            # Conexión directa SSL (Caso Gmail puerto 465)
            with smtplib.SMTP_SSL(config["server"], config["port"], timeout=10) as server:
                server.login(config["user"], config["password"])
                server.send_message(msg)
        else:
            with smtplib.SMTP(config["server"], config["port"], timeout=10) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(config["user"], config["password"])
                server.send_message(msg)
    except Exception as e:
        # Atrapamos absolutamente cualquier fallo (Errno 101, timeouts, etc.)
        print(f"Alerta de Red: Render no permite enviar mails con smtp, se debe usar una api externa. {e}", flush=True)
        # Retornamos True o simplemente pasamos para que el backend continúe limpio
        return False