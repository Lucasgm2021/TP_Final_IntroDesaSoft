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