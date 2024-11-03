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
def make_reservation():
    try:
        data = request.json
        new_reservation = Reservation(**data)
        db.session.add(new_reservation)
        db.session.commit()
        return jsonify({"message": "Reserva creada con éxito", "status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al crear reserva: {str(e)}", "status": "error"})
