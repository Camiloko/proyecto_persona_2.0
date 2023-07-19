"""User model."""

# Config
from app.config.mysql_connection import connect_to_mysql

# Models



class User:
    """Clase del modelo de usuario."""

    def __init__(self, data):
        """
        Constructor.

        El método `__init__()` es el constructor de la clase, se ejecuta cuando se crea
        una instancia de la clase. Las propiedades de la clase se definen en este método.

        Parámetros:
            self (object): Objeto de tipo `User`
            data (dict): Diccionario con los datos del usuario
        Retorna:
            None
        """

        self.id = data["id"]
        self.first_name = data["first_name"]
        self.email = data["email"]
        self.password = data["password"]

    @classmethod
    def get_by_email(cls, data):
        """
        Obtener usuario por email.
        """
            
        query = """
        SELECT *
        FROM users WHERE email = %(email)s;
        """
        results = connect_to_mysql().query_db(query, data)
    
        if results:
            return cls(results[0])
        return None
    
    @classmethod
    def register(cls, data):
        """
        Registro de usuario.
        """

        query = """
        INSERT INTO users (first_name, email, password)
        VALUES (%(first_name)s, %(email)s, %(password)s);
        """
        user_id = connect_to_mysql().query_db(query, data)
        data = {"user_id": user_id}

        if user_id:
            user = cls.get_one(data)
            return user
        return None

    
    @classmethod
    def get_one(cls, data):
        """
        Obtener un usuario.
        """

        query = """
        SELECT * FROM users WHERE id = %(id)s;
        """
        results = connect_to_mysql().query_db(query, data)
        if results:
            user = cls(results[0])
            return user

        return None