"""Viaje controllers."""

# Flask
from flask import render_template, redirect, request, url_for, session, jsonify
from datetime import datetime
import moment



# Config app
from app import app
import pandas as pd
from io import BytesIO

# Models
from app.models.gantt import Gantt

@app.route('/gantt', methods=['GET'])
def gantt():
    # Proteger la ruta /logout/
    if "user" not in session:
        return redirect(url_for("index"))
    
    return render_template('users/gantt_user.html')


@app.route('/guardar_tarea', methods=['POST'])
def guardar_tarea():
    data = request.json

    # Obtener los datos de la nueva tarea desde el objeto 'data'
    task_name = data.get('name')
    start_date = data.get('start')
    end_date = data.get('end')
    color = data.get('color')

    # Obtener el 'user_id' desde la sesión del usuario
    user_id = session['user']['id']

    # Crear el objeto Gantt y guardar la tarea en la base de datos
    new_task_data = {
        "user_id": user_id,
        "tarea": task_name,
        "fecha_inicio": start_date,
        "fecha_termino": end_date,
        "color": color
    }

    # Llamar al método 'create_gantt' de tu modelo Gantt para guardar la tarea
    new_task = Gantt.create_gantt(new_task_data)

    if new_task:
        # Devolver una respuesta de éxito con el ID de la nueva tarea guardada
        return jsonify({"id": new_task.id}), 200
    else:
        # Devolver una respuesta de error si no se pudo guardar la tarea
        return jsonify({"error": "No se pudo guardar la tarea"}), 500

@app.route('/actualizar_tarea', methods=['POST'])
def actualizar_tarea():
    data = request.json

    # Obtener los datos de la tarea modificada desde el objeto 'data'
    task_name = data.get('name')
    start_date= data.get('start')
    end_date= data.get('end')


    updated_task_data = {
        "user_id": session['user']['id'],
        "tarea": task_name,
        "fecha_inicio": start_date,
        "fecha_termino": end_date,
    }

    updated_task = Gantt.update_gantt(updated_task_data)

    if updated_task:
        return jsonify({"message": "Tarea actualizada correctamente"}), 200
    else:
        return jsonify({"error": "No se pudo actualizar la tarea"}), 500
    
@app.route('/obtener_tareas', methods=['GET'])
def obtener_tareas():
        # Aquí obtienes las tareas del usuario desde la base de datos
        user_id = session['user']['id']
        tasks = Gantt.get_gantt(user_id)

        # Devuelves las tareas en formato JSON
        return jsonify(tasks)

# Endpoint para obtener las tareas del usuario
@app.route('/get_user_tasks', methods=['GET'])
def get_user_tasks():
    user_id = session['user']['id']

    # Imprimir el valor de user_id para verificar que tenga el valor correcto
    

    user_tasks = Gantt.get_gantt({"user_id": user_id})

    # Imprimir los resultados de la consulta para depuración
    

    if user_tasks:
        return jsonify({"tasks": user_tasks}), 200
    else:
        return jsonify({"error": "No se encontraron tareas para el usuario"}), 404


# Endpoint para agregar una nueva tarea al usuario
@app.route('/add_user_task', methods=['POST'])
def add_user_task():
    data = request.json
    gantt_id = Gantt.create_gantt(data)
    if gantt_id:
        return jsonify({"message": "Tarea agregada correctamente"})
    else:
        return jsonify({"error": "No se pudo agregar la tarea"}), 500


@app.route('/eliminar_tarea', methods=['POST'])
def eliminar_tarea():
    try:
        # Obtener el ID de la tarea a eliminar desde los datos enviados por el cliente
        data = request.get_json()


        Gantt.eliminar_tarea(data)

        # Si la tarea se eliminó con éxito, enviar una respuesta exitosa al cliente
        response = {
            'message': 'Tarea eliminada exitosamente.'
        }
        return jsonify(response), 200

    except Exception as e:
        # Si ocurre algún error durante el proceso, enviar una respuesta de error al cliente
        response = {
            'error': 'Error al eliminar la tarea: ' + str(e)
        }
        return jsonify(response), 500


