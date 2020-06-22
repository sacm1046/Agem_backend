from flask import Blueprint, jsonify, request
from models import db, Client

client_route = Blueprint('client_route', __name__)
@client_route.route('/clients', methods=['GET','POST'])
@client_route.route('/client/<int:id>', methods=['GET','DELETE'])
def clients(id=None):
    if request.method == 'GET':
        if id is not None:
            client = Client.query.get(id)
            if client:
               return jsonify(client.serialize()), 200
            else:
                return jsonify({"client": "Not Found"})
        else:
            clients = Client.query.all()
            clients = list(map(lambda client: client.serialize(),clients))
            return jsonify(clients), 200
    
    if request.method == 'POST':
        name = request.json.get('name')
        email = request.json.get('email')
        phone = request.json.get('phone')
        if not name:
            return jsonify({"msg": "name is required"}), 422 
        if not email:
            return jsonify({"msg": "email is required"}), 422 
        if not phone:
            return jsonify({"msg": "phone is required"}), 422
        client = Client()
        client.name = name
        client.email = email
        client.phone = phone
        db.session.add(client)
        db.session.commit()
        return jsonify(client.serialize()), 201

    if request.method == 'DELETE':
        client = Client.query.get(id)
        db.session.delete(client)
        db.session.commit()
        return jsonify({'client':'Deleted'}), 200