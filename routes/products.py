from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import db, Product

product_route = Blueprint('product_route', __name__)
@product_route.route('/products', methods=['GET','POST'])
@product_route.route('/product/<int:id>', methods=['GET','PUT','DELETE'])
#@jwt_required
def products(id=None):
    if request.method == 'GET':
        if id is not None:
            product = Product.query.get(id)
            if product:
               return jsonify(product.serialize()), 200
            else:
                return jsonify({"product": "Not Found"})
        else:
            products = Product.query.all()
            products = list(map(lambda product: product.serialize(),products))
            return jsonify(products), 200
    
    if request.method == 'POST':
        name = request.json.get('name')
        price = request.json.get('price')
        duration = request.json.get('duration')
        if not name:
            return jsonify({"msg": "name is required"}), 422 
        if not price:
            return jsonify({"msg": "price is required"}), 422 
        if not duration:
            return jsonify({"msg": "duration is required"}), 422
        product = Product()
        product.name = name
        product.price = price
        product.duration = duration
        db.session.add(product)
        db.session.commit()
        return jsonify(product.serialize()), 201
    
    if request.method == 'PUT':
        product = Product.query.get(id)
        product.name = request.json.get('name')
        product.email = request.json.get('price')
        product.phone = request.json.get('duration')
        db.session.commit()
        return jsonify(product.serialize()), 200

    if request.method == 'DELETE':
        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({'product':'Deleted'}), 200