from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.reservations import Reservation
from config import db
from datetime import datetime

# Crea el Blueprint para reservaciones
reservations_bp = Blueprint("reservations", __name__)

# Ruta para obtener todas las reservas del usuario
@reservations_bp.route("/user_reservations", methods=["GET"])
@jwt_required()
def user_reservations():
    try:
        # Obtener el ID del usuario desde el token JWT
        user_id = get_jwt_identity()

        # Consultar las reservas del usuario
        reservations = Reservation.query.filter_by(user_id=user_id).all()

        # Renderizar la plantilla con las reservas del usuario
        return render_template("users/user_reservations.html", reservations=reservations)

    except Exception as e:
        print(f"Error al obtener las reservas: {e}")
        return jsonify({"message": "Error al cargar las reservas.", "status": "error"}), 500


# Ruta para crear una nueva reserva (POST)
@reservations_bp.route("/reservations", methods=["POST"])
@jwt_required()
def make_reservation():
    try:
        data = request.get_json()

        # Validación de campos requeridos
        required_fields = ["reservation_date", "num_people", "table_type", "terms_and_conditions_accepted"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "message": f"Faltan campos requeridos: {', '.join(missing_fields)}",
                "status": "error"
            }), 400

        # Validación de la fecha de reservación
        try:
            reservation_date = datetime.strptime(data["reservation_date"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify({
                "message": "Formato de fecha inválido. Use 'YYYY-MM-DD HH:MM:SS'.",
                "status": "error"
            }), 400

        # Validación del número de personas
        num_people = data["num_people"]
        if not isinstance(num_people, int) or num_people <= 0:
            return jsonify({
                "message": "El número de personas debe ser un entero positivo.",
                "status": "error"
            }), 400

        # Validación del tipo de mesa
        if data["table_type"] not in ["interior", "exterior"]:
            return jsonify({
                "message": "El tipo de mesa debe ser 'interior' o 'exterior'.",
                "status": "error"
            }), 400

        # Verificar aceptación de términos y condiciones
        if not data["terms_and_conditions_accepted"]:
            return jsonify({
                "message": "Debe aceptar los términos y condiciones.",
                "status": "error"
            }), 400

        # Obtener el ID del usuario desde el token JWT
        user_id = get_jwt_identity()

        # Crear una nueva reservación
        new_reservation = Reservation(
            user_id=user_id,
            reservation_date=reservation_date,
            num_people=num_people,
            table_type=data["table_type"],
            special_requests=data.get("special_requests"),
            terms_and_conditions_accepted=data["terms_and_conditions_accepted"],
            table_number=data.get("table_number")  # Opcional
        )

        # Guardar en la base de datos
        db.session.add(new_reservation)
        db.session.commit()

        return jsonify({"message": "Reserva creada con éxito", "status": "success"}), 201

    except Exception as e:
        print(f"Error al crear la reserva: {e}")
        db.session.rollback()
        return jsonify({"message": "Error interno del servidor. Intente nuevamente.", "status": "error"}), 500


# Ruta para editar una reserva existente (PUT)
@reservations_bp.route("/reservations/<int:reservation_id>", methods=["PUT"])
@jwt_required()
def edit_reservation(reservation_id):
    try:
        data = request.get_json()

        # Buscar la reserva en la base de datos
        reservation = Reservation.query.filter_by(
            reservation_id=reservation_id, user_id=get_jwt_identity()
        ).first()

        if not reservation:
            return jsonify({"message": "Reserva no encontrada.", "status": "error"}), 404

        # Actualizar los campos permitidos
        if "reservation_date" in data:
            reservation.reservation_date = datetime.strptime(data["reservation_date"], "%Y-%m-%d %H:%M:%S")
        if "num_people" in data:
            reservation.num_people = data["num_people"]
        if "table_type" in data and data["table_type"] in ["interior", "exterior"]:
            reservation.table_type = data["table_type"]
        if "special_requests" in data:
            reservation.special_requests = data["special_requests"]

        # Guardar cambios
        db.session.commit()
        return jsonify({"message": "Reserva actualizada con éxito.", "status": "success"}), 200

    except Exception as e:
        print(f"Error al editar la reserva: {e}")
        db.session.rollback()
        return jsonify({"message": "Error al actualizar la reserva.", "status": "error"}), 500


# Ruta para eliminar una reserva existente (DELETE)
@reservations_bp.route("/reservations/<int:reservation_id>", methods=["DELETE"])
@jwt_required()
def delete_reservation(reservation_id):
    try:
        # Buscar la reserva en la base de datos
        reservation = Reservation.query.filter_by(
            reservation_id=reservation_id, user_id=get_jwt_identity()
        ).first()

        if not reservation:
            return jsonify({"message": "Reserva no encontrada.", "status": "error"}), 404

        # Eliminar la reserva
        db.session.delete(reservation)
        db.session.commit()
        return jsonify({"message": "Reserva eliminada con éxito.", "status": "success"}), 200

    except Exception as e:
        print(f"Error al eliminar la reserva: {e}")
        db.session.rollback()
        return jsonify({"message": "Error al eliminar la reserva.", "status": "error"}), 500
