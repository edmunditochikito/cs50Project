from flask import Blueprint

# Crear un blueprint para las rutas
routes = Blueprint('routes', __name__)

# Importar los archivos de rutas
from .index import *
from .users import *
