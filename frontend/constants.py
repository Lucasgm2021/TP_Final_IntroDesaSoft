import os
print(os.getenv)
API_BASE_URL =  os.getenv('API_BASE_URL') or 'http://localhost:5000/'

#Configurado en app.py del backend con app.config["SESSION_COOKIE_NAME"] = "backend_session"
SESSION_COOKIE_NAME = os.getenv('SESSION_COOKIE_NAME') or 'backend_session'
FRONTEND_SESSION = os.getenv('FRONTEND_SESSION') or"usuario"

print("API_BASE_URL:", API_BASE_URL)
print("SESSION_COOKIE_NAME:", SESSION_COOKIE_NAME)
print("FRONTEND_SESSION:", FRONTEND_SESSION)