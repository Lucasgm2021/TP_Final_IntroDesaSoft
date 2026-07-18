from sqlalchemy import create_engine, text
from constants import DB_EXTERNAL_URI
# mysql+pymysql://usuario:password@host/db
engine = create_engine(
   DB_EXTERNAL_URI,
    connect_args={
        "ssl": {
            "ca": "/app/ca.pem" # Path to your downloaded Aiven certificate inside Docker
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
