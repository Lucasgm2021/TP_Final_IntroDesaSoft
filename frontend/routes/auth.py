from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    url_for
)

import requests
from constants import API_BASE_URL,BACKEND_SESSION_COOKIE_NAME, FRONTEND_COOKIE_CLAVE

auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@auth_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')

    resp = requests.post(
        f'{API_BASE_URL}/sesion/register',
        json={
            'email': request.form['email'],
            'password': request.form['password']
        }
    )

    if resp.status_code in (200, 201):
        session[FRONTEND_COOKIE_CLAVE] = resp.cookies.get(BACKEND_SESSION_COOKIE_NAME)
        return redirect(url_for("home.inicio"))
    elif resp.status_code == 409:
        return render_template('auth/register.html', error="Email ya utilizado")
    else:
        return render_template('auth/register.html', error=f"Error:{resp.status_code}")


@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    resp = requests.post(
        f'{API_BASE_URL}/sesion/login',
        json={
            'email': request.form['email'],
            'password': request.form['password']
        }
    )
    if resp.status_code == 201:
        session[FRONTEND_COOKIE_CLAVE] = resp.cookies.get(BACKEND_SESSION_COOKIE_NAME)
        return redirect(url_for("home.inicio"))
    else:
        return render_template('auth/login.html', error="Credenciales inválidas")

@auth_bp.route("/logout", methods=["GET","POST"])
def logout():
    data = session.get(FRONTEND_COOKIE_CLAVE) or ''
    requests.post(
        f'{API_BASE_URL}/sesion/logout',
        cookies={BACKEND_SESSION_COOKIE_NAME: data}
    )
    session.clear()
    return redirect(url_for("home.inicio"))