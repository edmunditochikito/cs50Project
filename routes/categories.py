from flask import Blueprint,jsonify
from config import db
from flask_jwt_extended import jwt_required
from models.categories import Category

category=Blueprint("category",__name__)

@category.route("/categories",methods=["POST"])
@jwt_required()
def all_categories():
    cate=db.session.execute(
        db.select(Category)
    ).scalars().all()
    
    cate = [{"name":catego.name,"id":catego.id} for catego in cate]
    return jsonify(cate)