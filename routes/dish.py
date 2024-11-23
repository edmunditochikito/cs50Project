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
    dishes = Dish.get_all()  
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

        
        dish_exist=db.session.execute(
            db.select(Dish).filter(Dish.name==name)
        ).scalars().first()
        if dish_exist:
            return jsonify({"message":"el platillo ya existe en la base de datos","status":"error"})
            
        
       
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
@admin.route('/updateDish/<id>', methods=[ 'POST'])
def edit_dish(id):
    """
    Ruta para editar un platillo existente
    """
    try:
        dish = Dish.query.get(id)
        print(dish)
        if not dish:
            return jsonify({"message":"el platillo no existe","status":"error"})
        
        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")
        category = request.form.get("category")
        
        dish.name = name
        dish.price = price
        dish.description = description
        dish.categories_id = category
        
        dish.save()
        return jsonify({"title":"Platillo actualizado correctamente","status":"success","message":f"el platillo {dish.name} ha sido actualizado con exito"})
    except Exception as e:
        return jsonify({"title":f"Ha ocurrido un error","status":"error","message":f"Error al actualizar el platillo {name}"})
 

        


# Ruta para eliminar un platillo
@admin.route('/deleteDish/<id>', methods=['POST'])
def delete_dish(id):
    """
    Ruta para eliminar un platillo
    """
    try:
        dish = Dish.query.get(id)
        if not dish:
            return jsonify({"status":"error","message":"no hemos podido eliminar el platillo ya que no existe","title":"platillo no encontrado"})
        name=dish.name
        dish.delete()
        return jsonify({"status":"success","message":f"el platillo {name} ha sido eliminado exitosamente","title":"platillo eliminado correctamente"})
    except Exception as e:
        return jsonify({"status":"error","message":""})
    

@admin.route("/getDishes",methods=["GET"])
def getDishes():
    
    dishes = db.session.execute(
        db.select(Dish)
    ).scalars().all()
    print(dishes)
    dishes=[{"id":dish.id,"name":dish.name,"price":dish.price,"description":dish.description,"image":dish.image} for dish in dishes]
    
    return jsonify({"data":dishes})

@admin.route("/getDish",methods=["POST"])
def getDish():
    data=request.json
    id=data["id"]
    
    dishes = db.session.execute(
        db.select(Dish).filter(Dish.id==id)
    ).scalars().all()
    dishes=[{"id":dish.id,"name":dish.name,"price":dish.price,"description":dish.description,"category":dish.categories_id} for dish in dishes]
    
    return jsonify(dishes)