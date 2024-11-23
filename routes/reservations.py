from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.reservations import Reservation
from models.table import Table  
from config import db
from datetime import datetime

# Crea el Blueprint para reservaciones
reservations_bp = Blueprint("reservations", __name__, url_prefix="/reservations")

# Ruta para ver las reservas del usuario
@reservations_bp.route("/user_reservations", methods=["GET"])
@jwt_required()
def user_reservations():
    try:
        # Obtener el ID del usuario desde el token JWT
        user_data = get_jwt_identity()
        user_id = user_data['id']  # Extrae solo el 'id' del diccionario

        # Consultar las reservas del usuario
        reservations = Reservation.query.filter_by(user_id=user_id).all()

        # Renderizar la plantilla con las reservas del usuario
        return render_template("users/user_reservations.html", reservations=reservations)

    except Exception as e:
        print(f"Error al obtener las reservas: {e}")
        return jsonify({"message": "Error al cargar las reservas.", "status": "error"}), 500

# Ruta para ver el formulario de agregar una nueva reserva
@reservations_bp.route("/add_reservation", methods=["GET"])
@jwt_required()
def add_reservation_page():
    try:
        # Obtener el ID del usuario desde el token JWT
        user_id = get_jwt_identity()['id']

        # Obtener las reservas del usuario y las mesas ocupadas
        reserved_tables = Reservation.query.with_entities(Reservation.table_id).all()
        reserved_tables = [table[0] for table in reserved_tables]  # Solo números de mesas ocupadas

        # Obtener las mesas disponibles
        available_tables = Table.query.filter(Table.availabillity == True, Table.id.notin_(reserved_tables)).all()

        return render_template("users/add_reservation.html", available_tables=available_tables)

    except Exception as e:
        print(f"Error al cargar las mesas disponibles: {e}")
        return jsonify({"message": "Error al cargar las mesas disponibles.", "status": "error"}), 500



# Ruta para agregar una nueva reserva (POST)
@reservations_bp.route("/reservations", methods=["POST"])
@jwt_required()
def make_reservation():
    try:
        # Obtener los datos del formulario
        data = request.form

        # Validación de los campos
        reservation_date = data.get("reservation_date")
        num_people = int(data.get("num_people"))
        table_type = data.get("table_type")
        table_id = int(data.get("table_id"))
        special_requests = data.get("special_requests")
        terms_and_conditions_accepted = bool(data.get("terms_and_conditions_accepted"))

        # Obtener el ID del usuario desde el token JWT
        user_id = get_jwt_identity()['id']

        # Verificar si la mesa seleccionada ya está ocupada
        existing_reservation = Reservation.query.filter_by(table_id=table_id).first()
        if existing_reservation:
            return jsonify({"message": "La mesa seleccionada ya está ocupada.", "status": "error"}), 400

        # Crear la nueva reserva
        new_reservation = Reservation(
            user_id=user_id,
            reservation_date=datetime.strptime(reservation_date, "%Y-%m-%dT%H:%M"),
            num_people=num_people,
            table_type=table_type,
            table_id=table_id,
            special_requests=special_requests,
            terms_and_conditions_accepted=terms_and_conditions_accepted
        )

        # Guardar en la base de datos
        db.session.add(new_reservation)
        db.session.commit()

        return jsonify({"message": "Reserva creada con éxito", "status": "success"}), 201

    except Exception as e:
        print(f"Error al crear la reserva: {e}")
        db.session.rollback()
        return jsonify({"message": "Error al crear la reserva.", "status": "error"}), 500


# Ruta para eliminar una reserva existente (DELETE)
@reservations_bp.route("/reservations/<int:reservation_id>", methods=["DELETE"])
@jwt_required()
def delete_reservation(reservation_id):
    try:
        # Buscar la reserva en la base de datos
        reservation = Reservation.query.filter_by(
            reservation_id=reservation_id, user_id=get_jwt_identity()['id']
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
