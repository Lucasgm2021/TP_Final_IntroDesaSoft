from sqlalchemy import create_engine, text
import os
from constants import DB_EXTERNAL_URI

possible_paths = [
    "/app/ca.pem",                          # Local Docker Container root
    "/opt/render/project/src/ca.pem",       # Render True Repo Root 
    "/opt/render/project/src/backend/ca.pem",# Render Root Directory fallback
    os.path.join(os.getcwd(), "ca.pem")     # Local standard execution path
]

cert_path = None
for path in possible_paths:
    if os.path.exists(path) and os.path.getsize(path) > 0:
        cert_path = path
        break

ssl_args = {}
if cert_path:
    try:
        # Read the cert contents directly into memory
        with open(cert_path, "r", encoding="utf-8") as f:
            cert_content = f.read().strip()
        
        print(f"🚀 Successfully read certificate contents from {cert_path}")
        
        # Pass the contents via raw string data to bypass path resolution bugs
        ssl_args = {
            "ssl": {
                "cadata": cert_content
            }
        }
    except Exception as e:
        print(f"⚠️ Error reading cert file: {e}")
        # Fallback to string path if reading contents fails
        ssl_args = {"ssl": {"ca": cert_path}}
else:
    print("⚠️ WARNING: No non-empty ca.pem found anywhere.")
    
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
