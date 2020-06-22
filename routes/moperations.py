from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import db, MOperation

moperation_route = Blueprint('moperation_route', __name__)
@moperation_route.route('/moperations', methods=['GET','POST'])
@moperation_route.route('/moperation/<int:id>', methods=['GET','DELETE'])
#@jwt_required
def moperations(id=None):
    if request.method == 'GET':
        if id is not None:
            moperation = MOperation.query.get(id)
            if moperation:
               return jsonify(moperation.serialize()), 200
            else:
                return jsonify({"Manual operation": "Not Found"}), 404
        else:
            moperations = MOperation.query.all()
            moperations = list(map(lambda moperation: moperation.serialize(),moperations))
            return jsonify(moperations), 200
    
    if request.method == 'POST':
        total = request.json.get('total')
        detail = request.json.get('detail')
        date = request.json.get('date')
        time = request.json.get('time')
        worker_id = request.json.get('worker_id')
        if not total:
            return jsonify({"msg": "total is required"}), 422 
        if not detail:
            return jsonify({"msg": "detail is required"}), 422
        if not date:
            return jsonify({"msg": "date is required"}), 422
        if not time:
            return jsonify({"msg": "time is required"}), 422
        if not worker_id:
            return jsonify({"msg": "worker_id is required"}), 422
        moperation = MOperation()
        moperation.total = total
        moperation.detail = detail
        moperation.date = date
        moperation.time = time
        moperation.worker_id = worker_id
        db.session.add(moperation)
        db.session.commit()
        return jsonify(moperation.serialize()), 201
    
    if request.method == 'DELETE':
        moperation = MOperation.query.get(id)
        db.session.delete(moperation)
        db.session.commit()
        return jsonify({'moperation':'Deleted'}), 200