"""grapifos model."""

# Config
from app.config.mysql_connection import connect_to_mysql
import json
import pandas as pd


class Gantt:
    """Clase del modelo de Gantt."""

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
        self.tarea = data["tarea"]
        self.fecha_inicio = data["fecha_inicio"]
        self.fecha_termino = data["fecha_termino"]
        self.progress = data["progress"]
        self.color = data ["color"]
    


    @classmethod
    def create_gantt(cls,data):
        """
        Crea un nuevo registro de diagrama gantt en la base de datos.
        """
        query = """
        INSERT INTO Gantt (user_id, tarea,fecha_inicio,fecha_termino,progress,color)
        VALUES (%(user_id)s, %(tarea)s,%(fecha_inicio)s,%(fecha_termino)s,%(progress)s,%(color)s,)
        """

        gantt_id=connect_to_mysql().query_db(query, data)
        data= {"gantt_id": gantt_id}

        if gantt_id:
            gantt = cls.get_one(data)
            return gantt
        return None