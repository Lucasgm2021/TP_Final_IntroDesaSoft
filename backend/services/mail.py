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

def enviar_mail_con_qr_mailjet(mail_destino,asunto,mail_data,ruta_template):
    #https://app.mailjet.com/ cuenta con mail personal, se pone en el from. Pendiente probar API. QR se envia adjunto en mail.

    mail_restaurante = os.getenv("MAIL_ACCOUNT")
    app_password = os.getenv("MAIL_PASS")
    mail_from = os.getenv("MAIL_FROM","lucas.gustavo.mino@gmail.com")
    mail_server = os.getenv("MAIL_SERVER","smtp.mailjet.com")
    mail_port = int(os.getenv("MAIL_PORT",2525))

    msg = MIMEMultipart("related")
    msg["From"] = mail_from
    msg["To"] = "lucasmio98@gmail.com"
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

    with smtplib.SMTP(mail_server, mail_port, timeout=5) as server:
        print("Connection established. Sending EHLO...")
        server.ehlo()
        
        print("Upgrading connection to STARTTLS...")
        server.starttls()  
        server.ehlo()
        
        print("Logging in...")
        server.login(mail_restaurante, app_password)
        
        print("Sending message...")
        server.send_message(msg)
            
    print("🚀 Mail sent successfully!")