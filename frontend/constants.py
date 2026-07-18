import os
API_BASE_URL = os.getenv('API_BASE_URL','http://127.0.0.1:5000') 

#BACKEND_SESSION_COOKIE_NAME es el nombre que flask le da a la cookie que devuelve (intenta devolver) el backend. Por defecto es session, si se modifica en backend, se modifica acá
BACKEND_SESSION_COOKIE_NAME = 'session'

#FRONTEND_COOKIE_CLAVE es el nombre de la clave con el que se guarda el id de sesion que devuelve el backend en la cookie del navegador.
#El nombre de la cookie que crea el frontend tambien es session pero NO refieren a lo mismo. La cookie guarda un formato tipo diccionario con clave FRONTEND_COOKIE_CLAVE y valor el id de sesion del backend. 
FRONTEND_COOKIE_CLAVE = 'session'

HTTP_GET = "GET"
HTTP_POST = "POST"
HTTP_PUT = "PUT"
HTTP_PATCH = "PATCH"
HTTP_DELETE = "DELETE"

HTTP_CODE_OK = 200
HTTP_CODE_CREATED = 201
HTTP_CODE_BAD_REQUEST = 400
HTTP_CODE_UNAUTHORIZED = 401
HTTP_CODE_NO_CONTENT = 204
HTTP_CODE_NOT_FOUND = 404
HTTP_CODE_CONFLICT = 409

TIMEOUT_REQUEST = 10

BASE_URL_FRONT = "puerto-hermoso"