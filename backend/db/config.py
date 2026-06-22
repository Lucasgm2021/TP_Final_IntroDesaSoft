from sqlalchemy import create_engine, text
from constants import MYSQL_DATABASE,MYSQL_ROOT_PASSWORD,DB_HOST,DB_PORT
# mysql+pymysql://usuario:password@host/db
engine = create_engine(
   f"mysql+pymysql://root:{MYSQL_ROOT_PASSWORD}@{DB_HOST}:{DB_PORT}/{MYSQL_DATABASE}?charset=utf8mb4",
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
