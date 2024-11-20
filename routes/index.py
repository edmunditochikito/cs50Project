from flask import Blueprint, render_template

# Crear el Blueprint para las rutas relacionadas con el índice
index = Blueprint("index", __name__)

# Datos del menú (pueden ser enviados desde la base de datos en el futuro)
menu_data = {
    "entradas": [
        {
            "title": "Sopa del día",
            "description": "Una sopa recién preparada con ingredientes frescos de temporada.",
            "price": 5.99,
            "image": "Sopa.jpg",
        },
        {
            "title": "Bruschettas clásicas",
            "description": "Pan tostado con tomate fresco, albahaca y aceite de oliva virgen extra.",
            "price": 6.50,
            "image": "Bruschettas clásicas.jpg",
        },
        {
            "title": "Alitas de pollo BBQ",
            "description": "Acompañadas de aderezo ranch y bastones de zanahoria y apio.",
            "price": 8.99,
            "image": "altas de pollo.jpg",
        },
    ],
    "platos-principales": [
        {
            "title": "Filete de res a la parrilla",
            "description": "Servido con papas al horno y vegetales salteados.",
            "price": 15.99,
            "image": "filetes res.jpg",
        },
        {
            "title": "Salmón al limón",
            "description": "Acompañado de arroz salvaje y ensalada fresca.",
            "price": 14.50,
            "image": "Salmon.jpg",
        },
        {
            "title": "Pasta Alfredo con pollo",
            "description": "Pasta al dente en una cremosa salsa Alfredo con trozos de pollo a la parrilla.",
            "price": 12.99,
            "image": "pasta.jpg",
        },
    ],
    "postres": [
        {
            "title": "Cheesecake de frutos rojos",
            "description": "Suave pastel de queso con una cubierta de frutos rojos.",
            "price": 5.50,
            "image": "Cheesecake.jpg",
        },
        {
            "title": "Brownie caliente con helado",
            "description": "Brownie de chocolate servido con helado de vainilla.",
            "price": 5.99,
            "image": "Brownie.jpeg",
        },
        {
            "title": "Mousse de maracuyá",
            "description": "Ligero y refrescante, ideal para finalizar la comida.",
            "price": 4.99,
            "image": "Mousse.jpg",
        },
    ],
    "bebidas": [
        {
            "title": "Limonada natural",
            "description": "Refrescante y hecha al momento.",
            "price": 2.50,
            "image": "Limonada.webp",
        },
        {
            "title": "Jugo de frutas",
            "description": "Preparado con fruta fresca (naranja, mango o piña).",
            "price": 3.00,
            "image": "JugoFrutas.jpg",
        },
        {
            "title": "Copa de vino tinto",
            "description": "Perfecto para acompañar carnes y pastas.",
            "price": 5.00,
            "image": "Vino.webp",
        },
    ],
}

@index.route("/")
def home():
    """
    Renderiza la página principal.
    """
    return render_template("index.html", menu=menu_data)
