"""User controllers."""

# Flask
from flask import render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt  
from datetime import datetime, timedelta


# Config app
from app import app

# Models
from app.models.users import User


# Bcrypt app
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    """
    Index page.

    La función `index()` es una función de vista, lo que significa que se
    ejecuta cuando el usuario visita la ruta / en el navegador.
    Ejemplo: http://localhost:5000/

    Parámetros:
        Ninguno
    Retorna:
        render_template: Renderiza la plantilla users/auth/index.html
    """

    return render_template("users/auth/index.html")





@app.route("/login/", methods=["POST"])
def login():
    """
    Iniciar sesión.

    La función `login()` es una función de vista, lo que significa que se
    ejecuta cuando el usuario da clic en el botón iniciar sesión.
    Ejemplo: http://localhost:5000/login/

    Parámetros:
        Ninguno
    Retorna:
        redirect: Redirecciona a la ruta /success/ si el usuario inicia sesión
    """

    data = {
        "email": request.form["email"],
        "password": request.form["password"]
    }
    
    user = User.get_by_email(data)

    if user:
        is_correct_password = bcrypt.check_password_hash(user.password, data["password"])
        if is_correct_password:
            user = {
                "id": user.id,
                "name": user.first_name,
                "email": user.email,
            }
            session["user"] = user
            flash("¡Bienvenido de nuevo!", "success")
            return redirect(url_for("upload"))
        
    flash("Email o contraseña incorrectos", "danger")
    return redirect(url_for("index"))


@app.route("/logout/")
def logout():
    """
    Cerrar sesión.

    La función `logout()` es una función de vista, lo que significa que se
    ejecuta cuando el usuario visita la ruta /logout/ en el navegador.
    Ejemplo: http://localhost:5000/logout/

    Parámetros:
        Ninguno
    Retorna:
        redirect: Redirecciona a la función `index()`
    """

    # Proteger la ruta /logout/
    if "user" not in session:
        return redirect(url_for("index"))

    session.clear()
    flash("¡Hasta luego!", "success")
    return redirect(url_for("index"))


@app.route("/register/", methods=["POST"])
def register(): 
    """
    Registrar usuario.

    La función `register()` es una función de vista, lo que significa que se
    ejecuta cuando el usuario da clic en el botón registrar.
    Ejemplo: http://localhost:5000/register/

    Parámetros:
        Ninguno
    Retorna:
        redirect: Redirecciona a la ruta /success/ si el usuario se registra
    """

    # Encriptar contraseña
    password_hash = bcrypt.generate_password_hash(request.form["password"])

    # Diccionario de datos para el modelo
    data = {
        "first_name": request.form["first_name"],
        "email": request.form["email"],
        "password": password_hash,
    }

    # Validar que el correo electrónico no esté registrado
    if User.get_by_email(data):
        flash("¡El correo electrónico ya está registrado!", "danger")
        return redirect(url_for("index"))
    
    #Validar que constraseña y confirmar contraseña sean iguales
    password = request.form["password"]
    confirm_password = request.form["password_confirm"]

    if password != confirm_password:
        flash("La contraseñas tienen que ser iguales.", "danger")
        return redirect(url_for("index"))
    
    if len(password) < 8:
        flash("La contraseña debe tener al menos 8 caracteres.", "danger")
        return redirect(url_for("index"))
    
    # Registrar usuario
    user = User.register(data)
    if user:
        session["user"] = {
            "id": user.id,
            "first_name": user.first_name,
            "email": user.email,
        }
        flash("¡Registro exitoso!", "success")
        return redirect(url_for("index"))
    
    return redirect(url_for("index"))


