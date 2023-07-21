"""grapifos model."""

# Config
from app.config.mysql_connection import connect_to_mysql
import json
import pandas as pd


class grafico:
    """Clase del modelo de grafico."""

    def __init__(self, data) -> None:
        """
        Constructor.

        El método `__init__()` es el constructor de la clase, se ejecuta cuando se crea
        una instancia de la clase. Las propiedades de la clase se definen en este método.

        Parámetros:
            self (object): Objeto de tipo `Favorite`
            data (dict): Diccionario con los datos del favorito
        Retorna:
            None
        """

        self.id = data["id"]
        self.user_id = data["user_id"]
        self.tipo = data["tipo"]

    


    @classmethod
    def create_graph(cls,data):
        """
        Crea un nuevo registro de gráfico en la base de datos.
        """
        query = """
        INSERT INTO graficos (user_id, tipo)
        VALUES (%(user_id)s, %(tipo)s)
        """

        connect_to_mysql().query_db(query, data)

    @classmethod
    def create_only_graph(cls, data):
        """
        Crea un nuevo registro de gráfico en la base de datos.
        """
        query = """
        INSERT INTO graficos (tipo)
        VALUES (%(tipo)s)
        """

        connect_to_mysql().query_db(query, data)

    @classmethod
    def process_excel(cls,datos, columna_x, columna_y, tipo_grafico):
            # Si solo se recibe una columna de datos, contar las categorías y generar el gráfico de pastel automáticamente
        

        if tipo_grafico == 'area':
            chart_config = {
                'type': 'line',
                'data': {
                    'labels': datos[columna_x].sort_values().tolist(),
                    'datasets': [{
                        'label': columna_y,
                        'data': datos[columna_y].tolist(),
                        'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                        'borderColor': 'rgba(75, 192, 192, 1)',
                        'borderWidth': 1,
                        'fill': 'origin'
                    }]
                },
                'options': {
                    'scales': {
                        'y': {
                            'beginAtZero': True
                        }
                    }
                }
            }
        elif tipo_grafico == 'lineas':
            chart_config = {
                'type': 'line',
                'data': {
                    'labels': datos[columna_x].sort_values().tolist(),
                    'datasets': [{
                        'label': columna_y,
                        'data': datos[columna_y].tolist(),
                        'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                        'borderColor': 'rgba(75, 192, 192, 1)',
                        'borderWidth': 1,
                        'fill': False
                    }]
                },
                'options': {
                    'scales': {
                        'y': {
                            'beginAtZero': True
                        }
                    }
                }
            }
            ##
        elif tipo_grafico == 'pastel':
           # Contar la frecuencia de cada categoría en columna_y
            conteo_categorias = datos[columna_y].value_counts()

            # Obtener las etiquetas (nombres de las categorías) y valores del gráfico de pastel
            labels = conteo_categorias.index.tolist()
            valores = conteo_categorias.values.tolist()

            # Gráfico de pastel
            chart_config = {
                'type': 'pie',
                'data': {
                    'labels': labels,
                    'datasets': [{
                        'data': valores,
                        'backgroundColor': ['rgba(75, 192, 192, 0.2)', 'rgba(255, 205, 86, 0.2)', 'rgba(255, 99, 132, 0.2)'],
                        'borderColor': ['rgba(75, 192, 192, 1)', 'rgba(255, 205, 86, 1)', 'rgba(255, 99, 132, 1)'],
                        'borderWidth': 1
                    }]
                }
            }
    
        elif tipo_grafico == 'barras':
            datos_agrupados = datos.groupby(columna_x)[columna_y].sum().tolist()
            if columna_y:
                chart_config = {
                    'type': 'bar',
                    'data': {
                        'labels': list(set(datos[columna_x].tolist())),
                        'datasets': [{
                            'label': columna_y,
                            'data': datos_agrupados,
                            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                            'borderColor': 'rgba(75, 192, 192, 1)',
                            'borderWidth': 1
                        }]
                    },
                    'options': {
                        'scales': {
                            'y': {
                                'beginAtZero': True
                            }
                        }
                    }
                }
            else:
                chart_config = {
                    'type': 'bar',
                    'data': {
                        'labels': list(set(datos[columna_x].tolist())),
                        'datasets': [{
                            'label': columna_x,
                            'data': datos[columna_x].tolist(),
                            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                            'borderColor': 'rgba(75, 192, 192, 1)',
                            'borderWidth': 1
                        }]
                    },
                    'options': {
                        'scales': {
                            'y': {
                                'beginAtZero': True
                            }
                        }
                    }
                }
        elif tipo_grafico == 'dispersion':
            chart_config = {
                'type': 'scatter',
                'data': {
                    'datasets': [{
                        'label': columna_y,
                        'data': [{'x': x, 'y': y} for x, y in zip(datos[columna_x], datos[columna_y])],
                        'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                        'borderColor': 'rgba(75, 192, 192, 1)',
                        'borderWidth': 1
                    }]
                },
                'options': {
                    'scales': {
                        'y': {
                            'beginAtZero': True
                        }
                    }
                }
            }

        # Convertir la configuración del gráfico a JSON
        chart_config_json = json.dumps(chart_config)

        return chart_config_json

    @classmethod
    def ranking_graficos(cls):
        query = """
            SELECT tipo, COUNT(*) AS total
            FROM graficos
            GROUP BY tipo
            ORDER BY total DESC
        """ 
        resultados = connect_to_mysql().query_db(query)
        ranking=[]
        if resultados:
            for row in resultados:
                ranking_graficos ={
                    'tipo_grafico': row['tipo'], 
                    'total': row['total']
                    }
                ranking.append(ranking_graficos)
        return ranking
