"""Viaje controllers."""

# Flask
from flask import render_template, redirect, request, url_for, session, flash
from datetime import datetime

# Config app
from app import app
import pandas as pd
from io import BytesIO

# Models
from app.models.graficos import grafico


@app.route("/upload")
def create_graph():
    """
    Página de creación de gráfico.
    """

    # Proteger la ruta /logout/
    if "user" not in session:
        return redirect(url_for("index"))

    return render_template("upload.html")


@app.route('/upload', methods=["POST"])
def upload():

    # Proteger la ruta /logout/
    if "user" not in session:
        return redirect(url_for("index"))
    

    archivo = request.files['archivo']
    columna_x = request.form['columna_x'] if 'columna_x' in request.form else None
    columna_y = request.form['columna_y'] if 'columna_y' in request.form else None
    tipo_grafico = request.form['tipo_grafico']
   
    if not columna_x:
        # Manejo de la ausencia de columna_y, por ejemplo, asignar un valor predeterminado
        columna_x = None

    # Leer el archivo de Excel en memoria
    datos = pd.read_excel(BytesIO(archivo.read()))

    # Obtener los datos de las columnas seleccionadas por el usuario
    if tipo_grafico == 'pastel':
        datos_grafico = datos[[columna_y]]
    else:
        datos_grafico = datos[[columna_x, columna_y]]

    # Procesar los datos y obtener la configuración del gráfico
    chart_config_json = grafico.process_excel(datos_grafico, columna_x, columna_y, tipo_grafico)

    # Verificar si hay un usuario conectado
    user_id = session['user']['id'] if 'user' in session and 'id' in session['user'] else None

    # Crear el gráfico en la base de datos
    if user_id:
        data = {
            "user_id": user_id,
            "tipo": tipo_grafico
        }
        grafico.create_graph(data)
    else:
        data = {
            "tipo": tipo_grafico
        }
        grafico.create_only_graph(data)
    return render_template('graph.html', chart_config_json=chart_config_json)


@app.route('/ranking_graficos', methods = ["GET"])
def ranking_graficos():

    # Proteger la ruta /logout/
    if "user" not in session:
        return redirect(url_for("index"))
    
    
    resultados = grafico.ranking_graficos()
    return render_template('ranking.html', ranking=resultados)


