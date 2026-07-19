# TP FINAL: RESTAURANTE PUERTO HERMOSO

Sistema web para restaurante como trabajo practico integrador de la materia Introduccion al desarrollo de software.

## Funcionalidades

### Vistas publicas (usuario sin autenticar)

- Pagina de inicio publica con informacion del restaurante y accesos a vistas publica de menu y reseñas existentes.
- Autenticacion y registro de usuarios basado en sesiones. Se almacenan las contraseñas encriptadas en la base de datos.

### Usuario cliente autenticado

- Creacion de reservas validando disponibilidad de las mesas segun fecha, hora y cantidad de comensales.
- Envío de notificacion via mail una vez creada la reserva con QR para escanear el dia de la reserva y confirmar la asistencia. El mail tambien permite cancelar la reserva.
- Posibilidad de escribir reseñas una vez finalizada la reserva.

### Usuario administrador

Acceso adicional a un panel de administrador con:

- ABM de mesas disponibles para reservar.
- ABM de platos del menu.
- Subida de imagenes a servicio externo para asocia a los platos.
- Visualizacion de todas las reseñas y posibilidad de aprobarlas o desaprobarlas. Solo las aprobadas seran visibles en la vista de inicio.
- ABM de la informacion del restaurante y servicios extra en la vista de inicio.
- Vistas de solo lectura: dashboard de reservas del dia y estadisticas del restaurante, listado de usuarios registrados y de todas las reservas realizadas. 

### Publicado a internet

- BBDD mysql publicada en [aiven.io](https://aiven.io/), se apaga si no se usa por un periodo de tiempo.
- Frontend y backend publicados como servicios en https://render.com/
urls: 
   1. backend: https://tp-final-introdesasoft.onrender.com
   2. frontend: https://tp-final-introdesasoft-1.onrender.com

Uso gratuito, consulta inicial puede demorarse ya que se apaga la instancia y debe iniciarse.

El envio de mails no funciona desde render con smtplib. Se debe migrar a uso de una API o revisar configuracion.

### App kivy

Pendiente, queda sin funcionar.

## Configuracion general

### 1. Variables de entorno

#### 1.1. Backend

Copiar `.env.example` a `.env`. Los defaults en constants.py funcionan para desarrollo local sin docker (ejecutando con terminal), excepto la contraseña para el envío de mails y la de supabase que se deben colocar en el .env. La configuracion default de envío de mails es gmail con app password.

```bash
cp .env.example .env
```

```
MYSQL_DATABASE=restaurante
MYSQL_ROOT_PASSWORD=1234
DB_HOST=localhost
DB_URI=mysql+pymysql://<pass>@<host>:<port>/<default db>?ssl_ca=/<path_for_docker>/ca.pem
FRONTEND_PORT=5001
URL_FRONT=
CUENTA_MAIL_LOGIN=tpintrodesasoftware@gmail.com
CUENTA_MAIL_FROM=tpintrodesasoftware@gmail.com
CONTRASENA_MAIL=
PUERTO_MAIL=465
SERVIDOR_MAIL=smtp.gmail.com
SERVICIO_MAIL=gmail_app_pass
SUPABASE_URL=https://bxsiebhagayfpbldmsud.supabase.co
SUPABASE_API_KEY=
BUCKET_NAME=menu-imagenes
```
Si se coloca DB_URI, no usa MYSQL_DATABASE, MYSQL_ROOT y DB_HOST.
Formato de DB_URI para uso de db externa en aiven.io. Si es local, se arma con las variables mencionadas en el codigo (se puede omitir en ese caso).

Si no se coloca URL_FRONT, la arma usando localhost + FRONTEND_PORT.

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

Con MySQL 8 corriendo en la maquina donde se ejecutará el sistema (normalmente en el puerto `3306` por default):

1. Crear la base de datos y cargar el esquema:

   ```bash
   # Linux / macOS / WSL
   mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS restaurante;"
   mysql -u root -p1234 < db/01_init_db.sql
   mysql -u root -p1234 < db/02_insert_datos.sql
   ```

   ```powershell
   # Windows PowerShell
   mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS restaurante;"
   Get-Content db\01_init_db.sql | mysql -u root -p1234
   Get-Content db\02_insert_datos.sql | mysql -u root -p1234
   ```

2. Verificar que las tablas se hayan creado correctamente:

   ```bash
   mysql -u root -p -e "USE restaurante; SHOW TABLES;"
   ```

### 4. Entorno virtual, instalacion y ejecucion

El proyecto incluye scripts de setup que crean el entorno virtual, instalan las dependencias y levantan la API. Ignorar si se levanta con docker.

**Bash**
```bash
chmod +x setup_virtualenvs.sh
bash setup_virtualenvs.sh
```
**bat**

En bat solo hacer doble click al script setup_virtualenvs.bat

<span style="font-size:20px; font-weight: bold;"> Dependencias</span>

Se listan a modo informativo las dependencias usadas en el proyecto:

**backend**
- Flask 
- flask-cors 
- Flask-SQLAlchemy 
- PyMySQL 
- Flask-Session 
- python-dotenv 
- qrcode 
- pillow
- supabase  

**frontend**

- Flask 
- requests 
- python-dotenv

## Configuracion envío de mails

El .env.example incluye como configuracion por defecto los parametros para gmail con app password.
La contraseña es el app password que se debe actualizar.

```
CUENTA_MAIL_LOGIN=tpintrodesasoftware@gmail.com
CUENTA_MAIL_FROM=tpintrodesasoftware@gmail.com
CONTRASEÑA_MAIL=
PUERTO_MAIL=465
SERVIDOR_MAIL=smtp.gmail.com
SERVICIO_MAIL=gmail_app_pass
```

Para mailjet se modifica a:

```
CUENTA_MAIL_LOGIN=9fe9a5af859e4fc89f336f8429ab4fab
CUENTA_MAIL_FROM=puerto.hermoso.info@gmail.com
CONTRASEÑA_MAIL=
PUERTO_MAIL=2525
SERVIDOR_MAIL=smtp.mailjet.com
SERVICIO_MAIL=mailjet_key
```
La cuenta mail login pasa a ser la API KEY y la contraseña es la secret key generada desde el usuario logeado puerto.hermoso.info@gmail.com en https://www.mailjet.com/
El mail enviado se ve logeado desde el usuario en la pagina y por supuesto, del usuario que lo recibe.

## Ejecucion

### 1. Flask en la terminal (bash o bat)

#### Bash
```bash
chmod +x execute.sh
bash execute.sh
```
#### bat

En bat solo hacer doble click al script execute.bat

### 2. Docker

Levantar los contenedores

```bash
docker compose up -d
```

Verificar que los contenedores esten listos (puede tardar unos segundos):

```bash
docker compose logs -f
# Buscar que la db tenga el msj healthy y la inicializacion de las apps de back y front con flask."
```

Apagar el contenedor manteniendo los datos en el volumen:

```bash
docker compose down
```

Apagar y **borrar** los datos (la proxima vez se vuelven a correr los scripts sql):

```bash
docker compose down -v
```

#### OBSERVACIONES PARA PRUEBAS

Tener en cuenta ademas que se puede hacer pruebas mixtas:

Levantar servicio front local y conectar con backend y db publicadas. 
Levantar front y backend local y conectar con db publicadas.

Se quitan depends_on entre servicios en yml para este fin y en backend se incluye: ./backend/ca.pem:/app/ca.pem:ro
El archivo ca.pem se descarga de la db publicada y se coloca dentro de la carpeta backend para conectar a la db publicada en aiven.io.

Para levantar ciertos servicios:

```bash
docker compose up <servicios>
```