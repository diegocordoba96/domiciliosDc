from flask_restful import Resource
from flask import jsonify, request
from .. import db
from main.models import RestauranteModel
from main.auth.decorators import role_required
from flask_jwt_extended import get_jwt_identity



class Restaurante(Resource):
    @role_required(roles=["Admin","Restaurante"])
    def get(self, id):
        restaurante = db.session.query(RestauranteModel).get_or_404(id)
        try:
            return restaurante.to_json()
        except:
            return 'Resource not found', 404

    @role_required(roles=["Admin"])
    def put(self, id):
        restaurante = db.session.query(RestauranteModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(restaurante, key, value)
        try:
            db.session.add(restaurante)
            db.session.commit()
            return restaurante.to_json(), 201
        except:
            return '', 404

    @role_required(roles=["Admin"])
    def delete(self, id):
        restaurante = db.session.query(RestauranteModel).get_or_404(id)
        try:
            db.session.delete(restaurante)
            db.session.commit()
        except:
            return '', 404




class Restaurantes(Resource):
    @role_required(roles=[" Admin"])
    def get(self):
        restaurantes = db.session.query(RestauranteModel).all()
        return jsonify({
            'Restaurantes': [restaurante.to_json() for restaurante in restaurantes]
        })
    
    @role_required(roles=["Admin"])
    def post(self):
        restaurante = RestauranteModel.from_json(request.get_json())
        db.session.add(restaurante)
        db.session.commit()
        return restaurante.to_json(), 201

