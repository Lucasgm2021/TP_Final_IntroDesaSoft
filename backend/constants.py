import os

CUENTA_MAIL_LOGIN = os.getenv("CUENTA_MAIL_LOGIN") or "tpintrodesasoftware@gmail.com"
CUENTA_MAIL_FROM = os.getenv("CUENTA_MAIL_FROM") or "tpintrodesasoftware@gmail.com"
CONTRASEÑA_MAIL =os.getenv("CONTRASEÑA_MAIL") or ""
PUERTO_MAIL = int(os.getenv("PUERTO_MAIL",0)) or 465
SERVIDOR_MAIL = os.getenv("SERVIDOR_MAIL") or "smtp.gmail.com"
URL_PAGINA_WEB=os.getenv("URL_PAGINA_WEB") or "http://localhost:5001"
SERVICIO_MAIL=os.getenv("SERVICIO_MAIL") or SERVICE_MAIL_GMAIL_APP_PASS
SERVICIO_MAIL_GMAIL_APP_PASS = "gmail_app_pass"
SERVICIO_MAIL_MAILJET = "mailjet_key"