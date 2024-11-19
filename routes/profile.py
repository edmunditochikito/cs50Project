from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User
from config import db
from werkzeug.security import generate_password_hash


profile_bp = Blueprint("profile", __name__)

# Ruta para ver el perfil de usuario
@profile_bp.route("/profile", methods=["GET"])
@jwt_required()
def view_profile():
    try:
        # Obtener el ID del usuario desde el token JWT
        user_id = get_jwt_identity()
        
        # Consultar el usuario en la base de datos usando el user_id
        user = User.query.get(user_id["id"])
        
        if user is None:
            return jsonify({"message": "Usuario no encontrado"}), 404
        
        # Renderizar el perfil del usuario
        return render_template("users/profile.html", user=user)
    except Exception as e:
        return jsonify({"message": f"Error al cargar perfil: {str(e)}"}), 500

# Ruta para actualizar el perfil del usuario
@profile_bp.route("/profile", methods=["POST"])
@jwt_required()
def update_profile():
    try:
        # Obtener el ID del usuario desde el token JWT
        user_id = get_jwt_identity()
        
        # Consultar el usuario en la base de datos usando el user_id
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"message": "Usuario no encontrado", "status": "error"}), 404

        # Obtener los datos del formulario JSON
        data = request.json
        user.name = data.get("name", user.name)
        user.phone = data.get("phone", user.phone)
        
        # Actualización de la contraseña si se proporciona
        new_password = data.get("password")
        if new_password:
            user.password = generate_password_hash(new_password)

        # Guardar cambios en la base de datos
        db.session.commit()
        return jsonify({"message": "Perfil actualizado con éxito", "status": "success"})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al actualizar perfil: {str(e)}", "status": "error"}), 500
    
        