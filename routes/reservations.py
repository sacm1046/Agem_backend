from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import db, Reservation

reservation_route = Blueprint('reservation_route', __name__)
@reservation_route.route('/reservations', methods=['GET','POST'])
@reservation_route.route('/reservation/<int:id>', methods=['GET','DELETE'])
#@jwt_required
def reservations(id=None):
    if request.method == 'GET':
        if id is not None:
            reservation = Reservation.query.get(id)
            if reservation:
               return jsonify(reservation.serialize()), 200
            else:
                return jsonify({"reservation": "Not Found"})
        else:
            reservations = Reservation.query.all()
            reservations = list(map(lambda reservation: reservation.serialize(),reservations))
            return jsonify(reservations), 200
    
    if request.method == 'POST':
        time = request.json.get('time')
        date = request.json.get('date')
        detail = request.json.get('detail')
        total = request.json.get('total')
        client_id = request.json.get('client_id')
        worker_id = request.json.get('worker_id')
        if not time:
            return jsonify({"error": "time is required"}), 422 
        if not date:
            return jsonify({"error": "date is required"}), 422 
        if not detail:
            return jsonify({"error": "detail is required"}), 422
        if not total:
            return jsonify({"error": "total is required"}), 422
        if not client_id:
            return jsonify({"error": "client_id is required"}), 422
        if not worker_id:
            return jsonify({"error": "worker_id is required"}), 422    
        reservation = Reservation()
        reservation.time = time
        reservation.date = date
        reservation.detail = detail
        reservation.total = total
        reservation.client_id = client_id
        reservation.worker_id = worker_id
        db.session.add(reservation)
        db.session.commit()
        return jsonify(reservation.serialize()), 201
    
    if request.method == 'DELETE':
        reservation = Reservation.query.get(id)
        db.session.delete(reservation)
        db.session.commit()
        return jsonify({'reservation':'Deleted'}), 200