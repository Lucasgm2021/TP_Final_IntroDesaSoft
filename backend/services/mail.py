import smtplib
from flask import jsonify
from email.mime.text import MIMEText
from email.mime.image import MIMEImage 
from email.mime.multipart import MIMEMultipart
import services.qr as qr
import os
from pathlib import Path

# Establish our secure base path
BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = BASE_DIR / "mail_reserva.html"
# Configuration
sender_email = os.getenv("MAIL_ACCOUNT")
app_password = os.getenv("MAIL_PASS")

def enviar_mail():
    receiver_email = "lmino@fi.uba.ar"
    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Test Email from Python"
    message.attach(MIMEText("This is a test email sent via Python.", "plain"))

    print("pwd:",app_password,type(app_password))
    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(message)
    return jsonify({"msg":"Mail enviado"}),200

def enviar_mail_con_qr():
    receiver_email = "lmino@fi.uba.ar"
    # Create message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Test Email from Python"
    qr_data = "HOLA MUNDO"
    url_boton = "URL-PARA-CANCELAR"

    cid_key = "unique_id"
    path_mail_template = TEMPLATE_PATH

    with open(path_mail_template, "r", encoding="utf-8") as file:
        raw_html_template = file.read()


    # 2. DYNAMICALLY INJECT DATA INTO THE PLACEHOLDERS
    # This replaces {recipient_name}, {qr_cid}, and {button_url} in the HTML file
    final_html_body = raw_html_template.format(
        recipient_name="Lucas",
        qr_cid=cid_key,
        button_url=url_boton
    )

    # Attach HTML layout
    msg_alternative = MIMEMultipart("alternative")
    msg_alternative.attach(MIMEText(final_html_body, "html"))
    msg.attach(msg_alternative)

    qr_bytes = qr.generate_qr_bytes(qr_data)
    image_mime = MIMEImage(qr_bytes, _subtype="png")
    
    image_mime.add_header("Content-ID", f"<{cid_key}>")
    image_mime.add_header("Content-Disposition", "inline", filename="qrcode.png")
    msg.attach(image_mime)

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

    return jsonify({"msg":"Mail enviado"}),200
