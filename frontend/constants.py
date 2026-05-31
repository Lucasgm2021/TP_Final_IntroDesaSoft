import os
API_BASE_URL =  os.getenv('API_BASE_URL') or 'http://localhost:5000/'

#Configurado en app.py del backend con app.config["SESSION_COOKIE_NAME"] = "backend_session"
SESSION_COOKIE_NAME = os.getenv('SESSION_COOKIE_NAME') or 'backend_session'
FRONTEND_SESSION = os.getenv('FRONTEND_SESSION') or"usuario"