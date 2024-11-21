from flask import Blueprint,jsonify
from config import db
from models.categories import Category

category=Blueprint("category",__name__)

@category.route("/categories",methods=["POST"])
def all_categories():
    cate=db.session.execute(
        db.select(Category)
    ).scalars().all()
    
    cate = [{"name":catego.name,"id":catego.id} for catego in cate]
    return jsonify(cate)