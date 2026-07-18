from constants import (
    HTTP_CODE_OK,
    HTTP_CODE_CREATED,
    HTTP_CODE_BAD_REQUEST,
    HTTP_CODE_UNAUTHORIZED,
    HTTP_CODE_NO_CONTENT,
    HTTP_CODE_NOT_FOUND,
    HTTP_CODE_CONFLICT,
    HTTP_CODE_INTERNAL_SERVER_ERROR
)

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

#este archivo no iria en services, quizas en una carpeta constants o utils.

# --- Authentication Errors ---
UNAUTHORIZED = {
    "code": HTTP_CODE_UNAUTHORIZED,
    "message": "User is not authenticated.",
    "description": "The request lacks valid authentication credentials."
}

_NOT_FOUND = {
    "code": HTTP_CODE_NOT_FOUND,
    "message": "Resource not found.",
    "description": "The requested resource was not found."
}

# --- System Errors ---
_INTERNAL_SERVER_ERROR = {
    "code": HTTP_CODE_INTERNAL_SERVER_ERROR,
    "message": "Internal server error.",
    "description": "An unexpected error occurred on our servers."
}

_BAD_REQUEST = {
    "code": HTTP_CODE_BAD_REQUEST,
    "message": "Bad request.",
    "description": "The request could not be understood or was missing required parameters."
}

def unauthorized(custom_desc=None):
    error = _UNAUTHORIZED.copy()  # Copy so we don't mutate the original
    if custom_desc:
        error["description"] = custom_desc
    return error

def server_error(custom_desc=None):
    error = _INTERNAL_SERVER_ERROR.copy()  # Copy so we don't mutate the original
    if custom_desc:
        error["description"] = custom_desc
    return error

def not_found(custom_desc=None):
    error = _NOT_FOUND.copy()  # Copy so we don't mutate the original
    if custom_desc:
        error["description"] = custom_desc
    return error

def bad_request(custom_msg=None,custom_desc=None):
    error = _BAD_REQUEST.copy()  # Copy so we don't mutate the original
    if custom_desc:
        error["description"] = custom_desc
    if custom_msg:
        error["message"] = custom_msg
    return error