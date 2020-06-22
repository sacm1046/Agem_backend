from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import db, ROperation

roperation_route = Blueprint('roperation_route', __name__)
@roperation_route.route('/roperations', methods=['GET','POST'])
@roperation_route.route('/roperation/<int:id>', methods=['GET','DELETE'])
#@jwt_required
def roperations(id=None):
    if request.method == 'GET':
        if id is not None:
            roperation = ROperation.query.get(id)
            if roperation:
               return jsonify(roperation.serialize()), 200
            else:
                return jsonify({"reserved operation": "Not Found"})
        else:
            roperations = ROperation.query.all()
            roperations = list(map(lambda roperation: roperation.serialize(),roperations))
            return jsonify(roperations), 200
    
    if request.method == 'POST':
        total = request.json.get('total')
        detail = request.json.get('detail')
        reservation_id = request.json.get('reservation_id')
        if not total:
            return jsonify({"msg": "total is required"}), 422 
        if not detail:
            return jsonify({"msg": "detail is required"}), 422
        if not reservation_id:
            return jsonify({"msg": "reservation_id is required"}), 422
        roperation = ROperation()
        roperation.total = total
        roperation.detail = detail
        roperation.reservation_id = reservation_id
        db.session.add(roperation)
        db.session.commit()
        return jsonify(roperation.serialize()), 201
    
    if request.method == 'DELETE':
        roperation = ROperation.query.get(id)
        db.session.delete(roperation)
        db.session.commit()
        return jsonify({'roperation':'Deleted'}), 200