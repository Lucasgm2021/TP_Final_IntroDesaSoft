from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

import requests

from servicesfront.verificaciones import usuario_es_valido, usuario_es_admin

auth_front_bp = Blueprint(
    "auth_front",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@auth_front_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')

    resp = requests.post(
        'http://localhost:5005/sesion/register',
        json={
            'email': request.form['email'],
            'password': request.form['password']
        }
    )

    if resp.status_code == 200:
        session['usuario'] = resp.cookies.get('session')
        return redirect('profile')
    else:
        return render_template('auth/register.html', error="Email ya utilizado")


@auth_front_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    resp = requests.post(
        'http://localhost:5005/sesion/login',
        json={
            'email': request.form['email'],
            'password': request.form['password']
        }
    )

    if resp.status_code == 200:
        session['usuario'] = resp.cookies.get('session')
        return redirect('profile')
    else:
        return render_template('auth/login.html', error="Credenciales inválidas")

@auth_front_bp.route("/logout")
def logout():
    data = session.get('usuario') or ''
    requests.post(
        'http://localhost:5005/sesion/logout',
        cookies={'session': data}
    )
    session.clear()
    return redirect('login')

@auth_front_bp.route("/profile")
def profile():
    if not usuario_es_valido():
        return redirect('login')
    else:
        return render_template('auth/profile.html',admin=usuario_es_admin())