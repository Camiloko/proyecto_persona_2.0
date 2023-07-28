from flask import Flask, render_template, request, session
from app.models.users import User
from app.models.perfiles import Perfil
from datetime import datetime

from app import app


@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if request.method == 'POST':
        user_id = session["user"]["id"]  # Obtener el user_id de la sesión o de la base de datos
        fecha_nacimiento = request.form['fecha_nacimiento']
        genero = request.form['genero']
        profesion = request.form['profesion']

        edad = calcular_edad(fecha_nacimiento)  # Calcular la edad del usuario

        perfil = {
            'user_id': user_id,
            'genero': genero,
            'profesion': profesion,
            'edad': edad  # Agregar la edad al perfil
        }

        Perfil.create_profile(perfil)

        return render_template('users/profile.html', perfil=perfil)
    
    elif request.method == 'GET':
        user_id = session["user"]["id"]
        perfil = Perfil.get_one({'user_id': user_id})  # Llama al método get_one para obtener el perfil
        return render_template('users/profile.html', perfil=perfil)
    
def calcular_edad(fecha_nacimiento):
    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Convertir la fecha de nacimiento a un objeto datetime
    fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")

    # Calcular la diferencia entre la fecha actual y la fecha de nacimiento
    edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

    return edad