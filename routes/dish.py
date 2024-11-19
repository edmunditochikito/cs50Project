from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.dish import Dish
from config import db

# Crear el Blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin')

# Ruta para la administración de platillos
@admin.route('/manage', methods=['GET'])
def manage_dishes():
    """
    Ruta para ver las opciones de administración de platillos
    """
    return render_template('users/manage_dishes.html')

# Ruta para ver todos los platillos
@admin.route('/view_dishes', methods=['GET'])
def view_dishes():
    dishes = Dish.get_all()  # Obtener todos los platillos desde la base de datos
    return render_template('users/view_dishes.html', dishes=dishes)

# Ruta para agregar un platillo
@admin.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    if request.method == 'POST':
        # Obtener los datos del formulario
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        category = request.form.get('category')
        image = request.form.get('image')

        # Crear un nuevo platillo
        new_dish = Dish(
            name=name,
            price=price,
            description=description,
            category=category,
            image=image
        )
        new_dish.save()
        flash("Platillo agregado exitosamente", "success")
        return redirect(url_for('users.view_dishes'))  # Redirige a la vista de platillos
    return render_template('users/add_dish.html')

# Ruta para eliminar un platillo
@admin.route('/delete_dish/<int:dish_id>', methods=['POST'])
def delete_dish(id):
    dish = Dish.query.get(id)
    if dish:
        dish.delete(id)
        flash("Platillo eliminado exitosamente", "success")
    return redirect(url_for('users.view_dishes'))  # Redirige a la vista de platillos
