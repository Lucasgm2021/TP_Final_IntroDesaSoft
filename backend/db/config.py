from sqlalchemy import create_engine, text

# mysql+pymysql://usuario:password@host/db
engine = create_engine(
   "mysql+pymysql://root:1234@db:3306/restaurante?charset=utf8mb4",
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
