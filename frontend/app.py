from flask import Flask, render_template,redirect, url_for, request, flash, session, make_response
from routes.reservas import reserva_bp
from services import sesion

from datetime import datetime, timedelta

app = Flask(__name__)
app.config["SECRET_KEY"] = "manzana"
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/examples")
def index():
    return render_template("examples/example.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        resultado = sesion.obtener_perfil(request.cookies)
        if "id_usuario" in resultado:
            flash('Ya tienes una sesión activa.', 'info')
            return redirect(url_for("reservas.crear_reserva_form"))
        return render_template("login.html")
    # Handle POST request for login logic here
    email = request.form.get("email")
    password = request.form.get("password")
    result = sesion.login(email,password)
    if result.get("ok"):
        # 1. Login successful, redirect to a different page or show success message
        flash('Usuario logueado correctamente', 'success')
        # 2. Prepare our redirect action to the next page
        redireccion = redirect(url_for("reservas.crear_reserva_form"))
        
        # 3. Turn it into a malleable Flask Response object
        flask_response = make_response(redireccion)
        expires_date = datetime.now() + timedelta(hours=24)

        for name, value in result["cookies"].items():
            flask_response.set_cookie(
                name, 
                value, 
                expires=expires_date,  # <-- Keeps it alive across tabs for 24 hours!
                httponly=True,
                samesite="Lax",
                path="/"
            )
        print("flask response:", flask_response,flask_response.headers)
        return flask_response
    else:
        # Login failed, show error messages
        for e in result.get('errores', ['Error al logear.']):
            print(e,type(e))
            flash(e, 'error')

    return redirect(url_for("login"))

app.register_blueprint(reserva_bp,url_prefix="/reservas")

if __name__ == "__main__":
    app.run(debug=True)