from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
app.config["SECRET_KEY"] = "manzana"
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)

@app.route("/examples")
def examples():
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
        session["sesion_id"] = result["cookies"].get("backend_session")
        return redirect(url_for("reservas.crear_reserva_form"))
    else:
        # Login failed, show error messages
        for e in result.get('errores', ['Error al logear.']):
            flash(e, 'error')

    return redirect(url_for("login"))

app.register_blueprint(reserva_bp,url_prefix="/reservas")

@app.route("/")
def inicio():
    error = request.args.get("error",None)
    return render_template("base.html",usuario_logueado=usuario_es_valido(),error=error)

app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
app.register_blueprint(auth_front_bp, url_prefix="/auth")

if __name__ == "__main__":
    app.run(debug=True)