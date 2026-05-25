import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage 
from email.mime.multipart import MIMEMultipart
import services.qr as qr
import os



def enviar_mail_con_qr(mail_destino,asunto,mail_data,ruta_template):
    #Envia un mail en base a un template html, insertando pares clave valor en el mismo. 
    #SOLO soporta una imagen, en este caso el QR.

    mail_restaurante = os.getenv("MAIL_ACCOUNT")
    app_password = os.getenv("MAIL_PASS")
    print("app password",app_password)
    msg = MIMEMultipart("related")
    msg["From"] = mail_restaurante
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

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(mail_restaurante, app_password)
        server.send_message(msg)