from app.config.mysql_connection import connectToMySQL
from app.models.users import User

class Perfil:
    """Clase del modelo de perfil."""

    def __init__(self, data):


        self.id = data["id"]
        self.profesion = data["profesion"]
        self.edad = data["edad"]
        self.graficos = data["graficos"]

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