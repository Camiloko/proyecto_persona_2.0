"""grapifos model."""

# Config
from app.config.mysql_connection import connect_to_mysql
from flask import session



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
        self.color = data ["color"]
    


    @classmethod
    def create_gantt(cls,data):
        """
        Crea un nuevo registro de diagrama gantt en la base de datos.
        """
        query = """
        INSERT INTO gantt (user_id, tarea,fecha_inicio,fecha_termino,color)
        VALUES (%(user_id)s, %(tarea)s,%(fecha_inicio)s,%(fecha_termino)s,%(color)s)
        """


        gantt_id=connect_to_mysql().query_db(query, data)
        data= {"gantt_id": gantt_id}

        if gantt_id:
            gantt = cls.get_one(data)
            return gantt
        return None
    
    @classmethod
    def update_gantt(cls, data):
        """
        Actualiza un registro de diagrama gantt en la base de datos.
        """

        query = """
            UPDATE gantt
            SET fecha_inicio = %(fecha_inicio)s,
                fecha_termino = %(fecha_termino)s
            WHERE tarea = %(tarea)s AND user_id = %(user_id)s
        """

        if 'tarea' not in data:
            raise ValueError("El diccionario 'data' debe contener el campo 'id'")

        result = connect_to_mysql().query_db(query, data)

        if result:
            updated_gantt = cls.get_one({"id": data["id"]})
            return updated_gantt
        return None

    
    @classmethod
    def get_one(cls, data):
        """
        Obtener datos gantt.
        """

        query = """
        SELECT * FROM gantt WHERE id = %(id)s;
        """
        results = connect_to_mysql().query_db(query, data)
        if results:
            gannt_data = cls(results[0])
            return gannt_data

        return None
    
    @classmethod
    def get_gantt(cls, data):
        """
        Obtener datos gantt.
        """

        query = """
        SELECT id,tarea,fecha_inicio,fecha_termino 
        FROM gantt WHERE user_id = %(user_id)s;
        """

        tasks = connect_to_mysql().query_db(query, data)

        return tasks
    
    @classmethod
    def eliminar_tarea(cls, data):
        """
        Eliminar una tarea por su ID.
        """

        query = """
        DELETE FROM gantt WHERE id = %(id)s;
        """

        # Ejecutar la consulta DELETE
        return connect_to_mysql().query_db(query, data)


