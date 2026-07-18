
from servicesfront.inicio import obtener_info_restaurante, obtener_servicios_extra, obtener_reseñas_aprobadas
from servicesfront.verificaciones import usuario_es_valido, usuario_es_admin
from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def inicio():
    user = usuario_es_valido()
    info = obtener_info_restaurante()
    admin = usuario_es_admin()
    reseñas = obtener_reseñas_aprobadas()
    servicios = obtener_servicios_extra()
    try:
        #mysql con docker no guarda bien la info con tildes y ñ. Lo corrijo para mostrar en html.
        info["historia"] = info["historia"].encode('latin-1').decode('utf-8')
    except:
        #si la info estaba ok, no da error al intentar la corrección, ignoro este caso.
        pass

    return render_template(
        "inicio/inicio.html",
        usuario_logueado=user,
        usuario_admin=admin,
        info=info,
        reseñas=reseñas,
        servicios=servicios,
    )