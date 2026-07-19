from sqlalchemy import create_engine, text
import os
import ssl
from constants import DB_URI, DB_CA_CERT_PATH

connect_args = {}

if os.path.exists(DB_CA_CERT_PATH) and os.path.getsize(DB_CA_CERT_PATH) > 0:
    try:
        with open(DB_CA_CERT_PATH, "r", encoding="utf-8") as f:
            cert_content = f.read().strip()
        
        print(f"Successfully read certificate from: {DB_CA_CERT_PATH}")
        
        context = ssl.create_default_context()
        context.load_verify_locations(cadata=cert_content)
        connect_args = {"ssl": context}
        print("SSL Context loaded successfully")
        
    except Exception as e:
        print(f"Error creating custom SSL context: {e}")
        connect_args = {"ssl": {"ca": DB_CA_CERT_PATH}}
else:
    print(f"WARNING: No certificate found at '{DB_CA_CERT_PATH}'. Connecting without custom SSL.")

engine = create_engine(
    DB_URI,
    connect_args=connect_args
)

def ejecutar_query_lectura(query, params=None):
    with engine.connect() as conn:
        resultado = conn.execute(text(query), params or ())
        return resultado.mappings().all()

def ejecutar_query_escritura(query, params=None):
    with engine.begin() as conn:
        resultado = conn.execute(text(query), params or ())
        return resultado.lastrowid
