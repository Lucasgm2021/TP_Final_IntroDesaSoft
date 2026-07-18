import os

#db conf
MYSQL_DATABASE=os.getenv("MYSQL_DATABASE","restaurante")
MYSQL_ROOT_PASSWORD=os.getenv("MYSQL_ROOT_PASSWORD","1234")
DB_PORT=3306
DB_HOST=os.getenv("DB_HOST","localhost")
DB_EXTERNAL_URI = os.getenv("DB_EXTERNAL_URI","")


#url front para mail
FRONTEND_PORT = os.getenv("FRONTEND_PORT","5001")
URL_PAGINA_WEB= f"http://127.0.0.1:{FRONTEND_PORT}"

#mail conf
CUENTA_MAIL_LOGIN=os.getenv("CUENTA_MAIL_LOGIN","tpintrodesasoftware@gmail.com")
CUENTA_MAIL_FROM=os.getenv("CUENTA_MAIL_FROM","tpintrodesasoftware@gmail.com")
CONTRASENA_MAIL =os.getenv("CONTRASENA_MAIL","")
PUERTO_MAIL=int(os.getenv("PUERTO_MAIL",465))
SERVIDOR_MAIL=os.getenv("SERVIDOR_MAIL","smtp.gmail.com")

SERVICIO_MAIL=os.getenv("SERVICIO_MAIL","gmail_app_pass")
SERVICIO_MAIL_GMAIL_APP_PASS="gmail_app_pass"
SERVICIO_MAIL_MAILJET="mailjet_key"

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME") or 'menu-imagenes'
