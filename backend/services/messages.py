def error_msg(code, message, level="error", description=""):
    return ({
        "errors": [
            {
                "code": code,
                "message": message,
                "level": level,
                "description": description
            }
        ]
    }, code)

def error_msg_lista(errores,code): 
    lista_errores = []
    for error in errores:
        lista_errores.append({ 
            "code": code,
            "message": error["message"],
            "level": "error",
            "description": error["description"]
        })  
    return ({
        "errors": lista_errores
    },code)

def paginacion_msg(res, limit, offset,total, end_point, type, code, data=None,):

    first_offset = 0
    prev_offset = max(offset - limit, 0)
    next_offset = offset + limit if (offset + limit) < total else offset
    last_offset = ((total - 1) // limit) * limit if total > 0 else 0
    links = {}
    string_parametros = ""

    if data:
        lista_parametros=[]
        for clave in data:
            lista_parametros.append(f"{clave}={data[clave]}")
        string_parametros = "&" + "&".join(lista_parametros)

    if offset > 0:
        links["_first"] = {"href": f"{end_point}?_offset={first_offset}&_limit={limit}" + string_parametros}
        links["_prev"]  = {"href": f"{end_point}?_offset={prev_offset}&_limit={limit}" + string_parametros}

    if offset + limit < total:
        links["_next"] = {"href": f"{end_point}?_offset={next_offset}&_limit={limit}" + string_parametros}
        links["_last"] = {"href": f"{end_point}?_offset={last_offset}&_limit={limit}" + string_parametros}

    return {f"{type}": res, "_links": links}, str(code)