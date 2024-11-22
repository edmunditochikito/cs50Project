from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User
from models.reservations import Reservation
from models.table import Table
from config import db

# Crear el Blueprint
admin_bp = Blueprint("admin_routes", __name__, url_prefix="/admin")

# Ruta para verificar autenticación
@admin_bp.route("/check-auth", methods=["GET"])
def check_auth():
    try:
        user_identity = get_jwt_identity()
        user = User.query.get(user_identity["id"])

        if user is None:
            return jsonify({"message": "Usuario no encontrado"}), 404

        if user.role != "administrator":
            return jsonify({"message": "Acceso denegado: No eres administrador"}), 403

        return redirect(url_for('admin_routes.manage_dishes'))  # Redirigir si es administrador

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500


# Dashboard del administrador
@admin_bp.route("/dashboard", methods=["GET"])
def dashboard():
    reservations = Reservation.query.all()
    tables = Table.query.all()
    return render_template("users/dashboard.html", reservations=reservations, tables=tables)

# Ver reservas
@admin_bp.route("/view-reservations", methods=["GET"])
def view_reservations():
    reservations = Reservation.query.all()
    return render_template("users/view_reservations.html", reservations=reservations)

# Gestionar mesas (agregar, editar, eliminar)
@admin_bp.route("/manage-tables", methods=["GET"])
def manage_tables():
    tables = Table.query.all()
    return render_template("users/manage_tables.html")

# Agregar mesa
@admin_bp.route("/add-table", methods=["GET", "POST"])
def add_table():
    if request.method == "POST":
        try:
            new_table = Table(
                code=request.form.get("code"),
                capacity=request.form.get("capacity"),
                type=request.form.get("type"),
                availabillity="availabillity" in request.form
            )
            db.session.add(new_table)
            db.session.commit()
            flash("Mesa agregada exitosamente.", "success")
            return redirect(url_for("admin_routes.manage_tables"))  # Redirigir al gestionar mesas

        except Exception as e:
            db.session.rollback()
            flash(f"Error al agregar la mesa: {e}", "danger")
            return redirect(url_for("admin_routes.add_table"))

    return render_template("users/add_table.html")

# Editar mesa
@admin_bp.route("/edit-table/<int:table_id>", methods=["GET", "POST"])
def edit_table(table_id):
    table = Table.query.get(table_id)
    if not table:
        flash("Mesa no encontrada.", "danger")
        return redirect(url_for("admin_routes.manage_tables"))  # Corregir el nombre del endpoint

    if request.method == "POST":
        try:
            table.code = request.form.get("code")
            table.capacity = request.form.get("capacity")
            table.type = request.form.get("type")
            table.availabillity = "availabillity" in request.form
            db.session.commit()
            flash("Mesa editada exitosamente.", "success")
            return redirect(url_for("admin_routes.manage_tables"))  # Redirigir al gestionar mesas
        except Exception as e:
            db.session.rollback()
            flash(f"Error al editar la mesa: {e}", "danger")
            return redirect(url_for("admin_routes.edit_table", table_id=table_id))

    return render_template("users/edit_table.html", table=table)

# Ruta para desactivar mesas
@admin_bp.route("/deactivate-table/<int:table_id>", methods=["POST"])
def deactivate_table(table_id):
    table = Table.query.get(table_id)
    if not table:
        flash("Mesa no encontrada.", "danger")
        return redirect(url_for("admin_routes.manage_tables"))  # Redirigir correctamente

    try:
        table.deactivate()  # Asumiendo que tienes un método deactivate() en tu modelo Table
        flash("Mesa desactivada exitosamente.", "success")
    except Exception as e:
        flash(f"Error al desactivar la mesa: {e}", "danger")

    return redirect(url_for("admin_routes.manage_tables"))  # Corregir redirección

