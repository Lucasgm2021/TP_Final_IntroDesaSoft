from sqlalchemy import create_engine, text
import os
from constants import DB_EXTERNAL_URI

possible_paths = [
    "/app/ca.pem",
    "/opt/render/project/src/ca.pem",
    "/opt/render/project/src/backend/ca.pem",
    os.path.join(os.getcwd(), "ca.pem")
]

cert_path = None
for path in possible_paths:
    if os.path.exists(path) and os.path.getsize(path) > 0:
        cert_path = path
        break

connect_args = {}

if cert_path:
    try:
        with open(cert_path, "r", encoding="utf-8") as f:
            cert_content = f.read().strip()
        
        print(f"🚀 Successfully read certificate contents from {cert_path}")
        
        # En PyMySQL, el sub-diccionario 'ssl' maneja directamente el contexto si usamos sslContext
        # Pero la forma más compatible sin romper su parser interno de diccionarios es armar un contexto nativo:
        import ssl
        context = ssl.create_default_context()
        context.load_verify_locations(cadata=cert_content)
        
        connect_args = {"ssl": context}
        print("✅ SSL Context loaded successfully with cadata")
        
    except Exception as e:
        print(f"⚠️ Error creating custom SSL context: {e}")
        # Si falla, dejamos que use el path tradicional como último recurso
        connect_args = {"ssl": {"ca": cert_path}}
else:
    print("⚠️ WARNING: No ca.pem found.")

# Creamos el engine pasando el objeto SSL Context directamente

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
