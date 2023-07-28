from app.config.mysql_connection import connect_to_mysql
from app.models.users import User

class Perfil:
    """Clase del modelo de perfil."""

    def __init__(self, data):


        self.id = data["id"]
        self.user_id = data["user_id"]
        self.profesion = data["profesion"]
        self.genero = data["genero"]
        self.edad = data["edad"]

    @classmethod
    def get_by_user_id(cls, user_id):

        query = """
        SELECT * FROM perfil WHERE user_id = %(user_id)s;
        """
        data = {"user_id": user_id}
        results = connect_to_mysql().query_db(query, data)

        if results:
            return cls(results[0])
        return None
    
    @classmethod
    def get_one(cls, data):
        """
        Obtener un perfile.
        """

        query = """
       SELECT profile.*, users.name
        FROM profile
        JOIN users ON profile.user_id = users.id
        WHERE profile.user_id = %(user_id)s;

        """
        results = connect_to_mysql().query_db(query, data)
        if results:
            user = cls(results[0])
            return user

        return None
    
    @classmethod
    def create_profile(cls, data):
        """
        Registro de usuario.
        """

        query = """
        INSERT INTO profile (user_id,profesion,genero, edad)
        VALUES (%(user_id)s, %(profesion)s, %(genero)s,%(edad)s);
        """
        perfil_id = connect_to_mysql().query_db(query, data)
        data = {"perfil_id": perfil_id}

        if perfil_id:
            perfil = cls.get_one(data)
            return perfil

        return None