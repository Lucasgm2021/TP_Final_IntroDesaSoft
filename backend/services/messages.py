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