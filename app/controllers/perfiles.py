from flask import Flask, render_template
from app.models.users import User
from app.models.perfiles import Perfil

@app.route('/profile/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    """Obtener el perfil de un usuario por su ID."""

    user = User.get_one({"id": user_id})

    if user:
        perfil = Perfil.get_by_user_id(user.id)

        if perfil:
            profile_data = {
                "id": perfil.id,
                "profesion": perfil.profesion,
                "edad": perfil.edad,
                "graficos": perfil.graficos,
            }
            return render_template('profile.html', profile_data=profile_data)