# TP FINAL: RESTAURANTE PUERTO HERMOSO

## Dependencias

backend: Flask flask-cors Flask-SQLAlchemy PyMySQL Flask-Session python-dotenv qrcode pillow  
frontend: Flask requests Flask-Session python-dotenv

## Configuracion general

### 1. Variables de entorno

#### 1.1. Backend

Copiar `.env.example` a `.env`. Los defaults en constants.py ya funcionan para desarrollo local sin docker (ejecutando con terminal), excepto la contraseña para el envío de mails que se debe colocar en el .env. La configuracion default de envío de mails es gmail con app password.

```bash
cp .env.example .env
```

```
MYSQL_DATABASE=restaurante
MYSQL_ROOT_PASSWORD=1234
DB_HOST=localhost
FRONTEND_PORT=5001
CUENTA_MAIL_LOGIN=tpintrodesasoftware@gmail.com
CUENTA_MAIL_FROM=tpintrodesasoftware@gmail.com
CONTRASEÑA_MAIL=
PUERTO_MAIL=465
SERVIDOR_MAIL=smtp.gmail.com
SERVICIO_MAIL=gmail_app_pass
```

#### 1.2. Frontend

Copiar `.env.example` a `.env`. El default en constants.py funciona para desarrollo local sin docker (ejecutando con terminal).

```bash
cp .env.example .env
```

```
API_BASE_URL=http://127.0.0.1:5000
```

### 2. Docker (recomendado)

`docker-compose.yml` levanta MySQL 8,  monta `db/01_init_db.sql` como script de inicializacion, creando las tablas e inserta datos de prueba `db/02_insert_datos.sql`. Luego de que la base de datos esté disponible, levanta los servicios de backend y de frontend.

Si no se usa docker, saltar y avanzar a los puntos 3 y 4 de la configuracion. Si se usa docker, se pueden ignorar los puntos 3 y 4 ya que docker gestiona en un contenedor la db e instala dependencias automaticamente en los contenedores del front y back.
Se **expone la app del front** con un puerto que se pasa por variable de entorno al yml, y la **db en el puerto 3307**. 


#### 2.1 Variables de entorno para docker
Copiar `.env.example` a `.env` de la raiz del proyecto. Si no se usa docker, ignorar ese .env.example.

```bash
cp .env.example .env
```

```
MYSQL_ROOT_PASSWORD=1234
FRONTEND_PORT=5001
```

#### 2.2 Variables de entorno Backend con docker

Editar en el .env del backend, para que apunte al servicio de db:

```
DB_HOST=db 
```

Asegurar tambien que el **FRONTEND_PORT** del .env de docker coincida con el del .env del backend.

#### 2.3 Variables de entorno Frontend con docker

Editar en el .env del frontend:

```
API_BASE_URL=http://backend:5000
```

### 3. Base de datos MySQL

Con MySQL 8 corriendo en tu maquina (puerto `3306` por default):

1. Crear la base de datos y cargar el esquema:

   ```bash
   # Linux / macOS / WSL
   mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS restaurante;"
   mysql -u root -p restaurante < db/01_init_db.sql
   mysql -u root -p restaurante < db/02_insert_datos.sql
   ```

   ```powershell
   # Windows PowerShell
   mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS restaurante;"
   Get-Content db\01_init_db.sql | mysql -u root -p restaurante
   Get-Content db\02_insert_datos.sql | mysql -u root -p restaurante
   ```

2. Verificar que las tablas se hayan creado:

   ```bash
   mysql -u root -p -e "USE restaurante; SHOW TABLES;"
   ```

3. Si el usuario, password, puerto o nombre de base no coinciden con los defaults, actualizar el `.env` antes de levantar la API.

### 4. Entorno virtual, instalacion y ejecucion

**VER** El proyecto incluye scripts de setup que crean el entorno virtual, instalan las dependencias y levantan la API. Ignorar si se usa docker

Instalar dependencias en entornos virtuales (uno por back y otro por frontend). Se puede simplificar en un solo entorno virtual, ambas apps usan python con flask con misma version.

**Con virtualenv:**

#### 4.1 2 Entornos virtuales

```bash
cd /backend 
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
deactivate

cd ../frontend 
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
deactivate
```

#### 4.2 1 entorno virtual
```bash
python3 -m venv .venv
. .venv/bin/activate
cd /backend
pip install -r requirements.txt
cd ../frontend
pip install -r requirements.txt
deactivate
```

## Configuracion envío de mails

**PENDIENTE**

## Ejecucion

### 1. Flask en la terminal (bash)

#### 1.1 Con 2 Entornos virtuales

```bash
cd /backend 
. .venv/bin/activate
flask run --debug
cd ../frontend
. .venv/bin/activate
flask run --debug --port 5001
```
#### 1.2 Con 1 Entorno virtual

```bash
. .venv/bin/activate
cd /backend
flask run --debug

cd ../frontend
flask run --debug --port 5001
```

### 2. Docker

Levantar los contenedores

```bash
docker compose up -d
```

Verificar que los contenedores esten listos (puede tardar unos segundos):

```bash
docker compose logs -f
# Buscar que la db esté healthy y la inicializacion de las apps de back y front con flask."
```

Apagar el contenedor manteniendo los datos en el volumen:

```bash
docker compose down
```

Apagar y **borrar** los datos (la proxima vez se vuelven a correr los scripts sql):

```bash
docker compose down -v
```