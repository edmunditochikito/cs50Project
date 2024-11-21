from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from werkzeug.utils import secure_filename  
import os
from models.dish import Dish
from config import db

# Crear el Blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/images'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@admin.route('/manage', methods=['GET'])
def manage_dishes():

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
    if request.method=="POST":
        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")
        category = request.form.get("categories_id")
        image = request.files.get("image")
        print(image)
        print(request.form)
        
        # Validación del archivo
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            # Crear el directorio si no existe
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            # Guardar el archivo en el servidor
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(file_path)

            # Guardar los datos del platillo en la base de datos
            relative_path = f"{UPLOAD_FOLDER}/{filename}"
            new_dish = Dish(
                name=name,
                price=price,
                description=description,
                categories_id=category,
                image=relative_path
            )
            new_dish.save()

            return jsonify({"message": "Platillo agregado exitosamente","status":"success"})
        else:
            return jsonify({"message": "Archivo no permitido o faltante","status":"error"}),
    else:
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
