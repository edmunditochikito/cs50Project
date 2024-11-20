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
    """
    Ruta para listar todos los platillos
    """
    dishes = Dish.get_all()  # Método definido en el modelo
    return render_template('users/view_dishes.html', dishes=dishes)

# Ruta para agregar un platillo
@admin.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    """
    Ruta para agregar un nuevo platillo
    """
    if request.method == 'POST':
        # Obtener los datos del formulario
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        category = request.form.get('category')
        image = request.form.get('image')

        # Validar campos requeridos
        if not all([name, price, category]):
            flash("Todos los campos obligatorios deben completarse", "danger")
            return redirect(url_for('admin.add_dish'))

        # Crear un nuevo platillo
        new_dish = Dish(
            name=name,
            price=price,
            description=description,
            categories_id=category,
            image=image
        )
        try:
            new_dish.save()
            flash("Platillo agregado exitosamente", "success")
            return redirect(url_for('admin.view_dishes'))
        except Exception as e:
            flash(f"Error al guardar el platillo: {e}", "danger")
            return redirect(url_for('admin.add_dish'))
    return render_template('users/add_dish.html')

# Ruta para editar un platillo
@admin.route('/edit_dish/<int:dish_id>', methods=['GET', 'POST'])
def edit_dish(dish_id):
    """
    Ruta para editar un platillo existente
    """
    dish = Dish.query.get(dish_id)
    if not dish:
        flash("El platillo no existe", "danger")
        return redirect(url_for('admin.view_dishes'))
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        category = request.form.get('category')
        image = request.form.get('image')

        # Validar campos requeridos
        if not all([name, price, category]):
            flash("Todos los campos obligatorios deben completarse", "danger")
            return redirect(url_for('admin.edit_dish', dish_id=dish_id))
        
        # Actualizar los datos del platillo
        dish.name = name
        dish.price = price
        dish.description = description
        dish.categories_id = category
        dish.image = image

        try:
            dish.save()
            flash("Platillo actualizado exitosamente", "success")
            return redirect(url_for('admin.view_dishes'))
        except Exception as e:
            flash(f"Error al actualizar el platillo: {e}", "danger")
            return redirect(url_for('admin.edit_dish', dish_id=dish_id))
    
    # Mostrar el formulario de edición con los datos actuales
    return render_template('users/edit_dish.html', dish=dish)


# Ruta para eliminar un platillo
@admin.route('/delete_dish/<int:dish_id>', methods=['POST'])
def delete_dish(dish_id):
    """
    Ruta para eliminar un platillo
    """
    dish = Dish.query.get(dish_id)
    if dish:
        try:
            dish.delete()
            flash("Platillo eliminado exitosamente", "success")
        except Exception as e:
            flash(f"Error al eliminar el platillo: {e}", "danger")
    else:
        flash("El platillo no existe", "danger")
    return redirect(url_for('admin.view_dishes'))
