from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User
from models.reservations import Reservation
from models.table import Table
from config import db

# Crear el Blueprint
admin_bp = Blueprint("admin_routes", __name__, url_prefix="/admin")

# Dashboard del administrador

# Ver reservas
@admin_bp.route("/view-reservations", methods=["GET"])
def view_reservations():
    reservations = Reservation.query.all()
    return render_template("users/view_reservations.html", reservations=reservations)

# Gestionar mesas (agregar, editar, eliminar)
@admin_bp.route("/manage-tables", methods=["GET"])
@jwt_required()
def manage_tables():
    user=get_jwt_identity()
    tables = Table.query.all()
    if user["role"]=="administrator":
        return render_template("users/manage_tables.html")
    else: return redirect("/")
 

# Agregar mesa
@admin_bp.route("/add-table", methods=["GET", "POST"])
@jwt_required()
def add_table():
    user=get_jwt_identity()
    if request.method == "POST":
        try:
            data=request.json
            new_table=Table(code=data["code"],capacity=data["capacity"],type=data["type"])
            new_table.save()
            print(new_table.serialize())
            return jsonify({"message":"se agrego una nueva mesa con exito","status":"success"})
        except Exception as e:
           
            return jsonify({"message":f"error al agregar la mesa","status":"error"})
    else:
       if user["role"]=="administrator":
           return render_template('users/add_table.html')
       else: 
           return redirect("/")

# Editar mesa
@admin_bp.route("/updateTable/<id>", methods=["GET", "POST"])
def updateTable(id):
    try:
        table=Table.query.get(id)
        if not table:
            return jsonify({"message":"la mesa no existe","status":"error"})
        code = request.form.get("code")
        capacity = request.form.get("capacity")
        type = request.form.get("type")
        availabillity = request.form.get("availabillity", "").strip().lower() in ["true", "1"]
        
        table.code = code
        table.capacity = capacity
        table.type = type
        table.availabillity = availabillity
        
        table.save()
        
        return jsonify({"title":"Mesa actualizada correctamente","status":"success","message":f"la mesa con el codigo {code} ha sido actualizada con exito"})
    except Exception as e:
        return jsonify({"title":f"Ha ocurrido un error","status":"error","message":f"Error al actualizar la mesa con el codigo {code},{e}"})


# Ruta para desactivar mesas
@admin_bp.route("/deactivate-table/<id>", methods=["POST"])
def deactivate_table(id):
    try:
        table = Table.query.get(id)
        if not table:
            return jsonify({"status":"error","message":"no hemos podido desactivar la mesa ya que no existe","title":"mesa no encontrada"})
        code = table.code
        table.deactivate()
        return jsonify({"status":"success","message":f"la mesa con el codigo {code} ha sido desactivada exitosamente","title":"mesa desactivada correctamente"})
    except Exception as e:
        return jsonify({"status":"error","message":"Error","title":"error"})
    
@admin_bp.route("/getTables", methods=["GET"])
def getTables():
    tables=db.session.execute(
        db.select(Table)
    ).scalars().all()
    tables=[table.serialize() for table in tables]
    return jsonify({"data":tables})

@admin_bp.route("/getTable/<id>", methods=["GET"])
def getTable(id):
    table=db.session.execute(
        db.select(Table).filter(Table.id==id)
    ).scalars().all()
    table=[table.serialize() for table in table]
    return jsonify(table[0])

