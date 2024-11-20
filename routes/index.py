from flask import Blueprint, render_template
from models.dish import Dish  # Modelo de platillo
from models.categories import Category  # Modelo de categoría
from config import db

# Crear el Blueprint para las rutas relacionadas con el índice
index = Blueprint("index", __name__)

@index.route("/")
def home():
    """
    Renderiza la página principal, obteniendo los platillos categorizados por tipo.
    """
    # Diccionario para almacenar los platos por categoría
    categorized_dishes = {}

    # Obtener todas las categorías de la base de datos
    categories = db.session.execute(db.select(Category)).scalars().all()

    # Para cada categoría, buscar los platos relacionados
    for category in categories:
        dishes = (
            db.session.execute(
                db.select(Dish).filter(Dish.categories_id == category.id)
            )
            .scalars()
            .all()
        )
        # Serializar los datos de los platillos
        serialized_dishes = [
            {
                "name": dish.name,
                "price": float(dish.price),
                "description": dish.description,
                "image": dish.image,
            }
            for dish in dishes
        ]
        categorized_dishes[category.name] = serialized_dishes

    # Mostrar los datos serializados en consola para depuración
    print(categorized_dishes)

    # Renderizar la página principal y pasar los datos categorizados
    return render_template("index.html", categorized_dishes=categorized_dishes)
