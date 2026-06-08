import os
API_BASE_URL = os.getenv('API_BASE_URL') or 'http://127.0.0.1:5005/'

#Configurado en app.py del backend con app.config["BACKEND_SESSION_COOKIE_NAME"] = "backend_session"
BACKEND_SESSION_COOKIE_NAME = os.getenv('BACKEND_SESSION_COOKIE_NAME') or 'backend_session'
FRONTEND_COOKIE_CLAVE = os.getenv('FRONTEND_COOKIE_CLAVE') or "usuario"