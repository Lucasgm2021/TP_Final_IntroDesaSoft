from sqlalchemy import create_engine, text
import os
from constants import DB_EXTERNAL_URI

# os.getcwd() gets the root folder where the app started running (the backend/ folder)
# This works perfectly both on Render and inside your local Docker container!
# Define all possible physical paths where ca.pem could live
possible_paths = [
    "/app/ca.pem",                          # Local Docker Container root
    "/opt/render/project/src/ca.pem",       # Render True Repo Root 
    "/opt/render/project/src/backend/ca.pem",# Render Root Directory fallback
    os.path.join(os.getcwd(), "ca.pem")     # Local standard execution path
]

cert_path = None
for path in possible_paths:
    # Ensure the path exists AND has content inside it (> 0 bytes)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        cert_path = path
        break

if cert_path:
    print(f"🚀 Found valid SSL certificate at: {os.path.abspath(cert_path)}")
else:
    # If it falls back to this, the file on Render is definitely empty or missing!
    cert_path = os.path.join(os.getcwd(), "ca.pem")
    print("⚠️ WARNING: No non-empty ca.pem found. Falling back to default current directory path.")

engine = create_engine(
    DB_EXTERNAL_URI,
    connect_args={
        "ssl": {
            "ca": cert_path
        }
    }
)

engine = create_engine(
   DB_EXTERNAL_URI,
    connect_args={
        "ssl": {
            "ca": cert_path # Path to your downloaded Aiven certificate inside Docker
        }
    },
    echo=False
)


def ejecutar_query_lectura(query, params=None):
    with engine.connect() as conn:
        resultado = conn.execute(text(query), params or ())
        return resultado.mappings().all()

def ejecutar_query_escritura(query, params=None):
    with engine.begin() as conn:
        resultado = conn.execute(text(query), params or ())
        return resultado.lastrowid
