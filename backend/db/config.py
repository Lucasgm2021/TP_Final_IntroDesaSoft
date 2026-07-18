from sqlalchemy import create_engine, text
import os
from constants import DB_EXTERNAL_URI

# os.getcwd() gets the root folder where the app started running (the backend/ folder)
# This works perfectly both on Render and inside your local Docker container!
cert_path = os.path.join(os.getcwd(), "ca.pem")

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
