# reservations.py
from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required
from models.reservations import Reservation  
from config import db

# Crea el Blueprint para reservaciones
reservations_bp = Blueprint("reservations", __name__)

# Ruta para mostrar el formulario de reservaciones
@reservations_bp.route("/reservations", methods=["GET"])
@jwt_required()
def show_reservation_form():
    return render_template("users/reservation.html")  

# Ruta para procesar la reserva (POST)
@reservations_bp.route("/reservations", methods=["POST"])
@jwt_required()
def make_reservation():
    try:
        data = request.json
        
        # Validación de campos requeridos
        required_fields = ["user_id", "reservation_date", "num_people", "table_type", "terms_and_conditions_accepted"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"message": f"Faltan campos requeridos: {', '.join(missing_fields)}", "status": "error"}), 400

        # Crea la nueva instancia de reservación
        new_reservation = Reservation(
            user_id=data["user_id"],
            reservation_date=data["reservation_date"],
            num_people=data["num_people"],
            table_type=data["table_type"],
            special_requests=data.get("special_requests"),  
            terms_and_conditions_accepted=data["terms_and_conditions_accepted"],
            table_number=data.get("table_number") 
        )

        # Agrega y guarda la nueva reservación en la base de datos
        db.session.add(new_reservation)
        db.session.commit()
        
        return jsonify({"message": "Reserva creada con éxito", "status": "success"})
    
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": f"Error al crear reserva: {str(e)}", "status": "error"}), 500
