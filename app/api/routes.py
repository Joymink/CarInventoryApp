from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Inventory, inventory_schema, inventories_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/inventory', methods= ['POST'])
@token_required
def create_vehicle(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    price = request.json['price']
    user_token = current_user_token.token

    print(f'TESTER: {current_user_token.token}')

    inventory = Inventory(make, model, year, price, user_token = user_token)

    db.session.add(inventory)
    db.session.commit()

    response = inventory_schema.dump(inventory)
    print(response)
    return jsonify(response)

@api.route('/inventory', methods = ['GET'])
@token_required
def get_vehicle(current_user_token):
    a_user = current_user_token.token
    vehicles = Inventory.query.filter_by(user_token = a_user).all()
    response = inventories_schema.dump(vehicles)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['GET'])
@token_required
def get_single_vehicle(current_user_token, id):
    vehicle = Inventory.query.get(id)
    response = inventory_schema.dump(vehicle)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['POST','PUT'])
@token_required
def update_vehicle(current_user_token, id):
    vehicle = Inventory.query.get(id)
    vehicle.make = request.json['make']
    vehicle.model = request.json['model']
    vehicle.year = request.json['year']
    vehicle.price = request.json['price']
    vehicle.user_token = current_user_token.token

    db.session.commit()
    response = inventory_schema.dump(vehicle)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['DELETE'])
@token_required
def delete_vehicle(current_user_token, id):
    vehicle = Inventory.query.get(id)
    db.session.delete(vehicle)
    db.session.commit()
    response = inventory_schema.dump(vehicle)
    return jsonify(response)


