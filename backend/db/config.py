from sqlalchemy import create_engine, text

# mysql+pymysql://usuario:password@host/db
engine = create_engine(
    "mysql+pymysql://root:1234@127.0.0.1/restaurante",
    echo=False,
    future=True
)


def ejecutar_query_lectura(query, params=None):
    with engine.connect() as conn:
        resultado = conn.execute(text(query), params or ())
        return resultado.mappings().all()

def ejecutar_query_escritura(query, params=None):
    with engine.begin() as conn:
        resultado = conn.execute(text(query), params or ())
        return resultado.lastrowid
