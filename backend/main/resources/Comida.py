from flask_restful import Resource
from flask import jsonify, request
from .. import db
from main.models import ComidaModel
from main.auth.decorators import role_required
from flask_jwt_extended import get_jwt_identity



class Comida(Resource):
    @role_required(roles=["Admin","Restaurante"])
    def get(self, id):
        comida = db.session.query(ComidaModel).get_or_404(id)
        try:
            return comida.to_json()
        except:
            return 'Resource not found', 404

    @role_required(roles=["Admin","Restaurante"])
    def put(self, id):
        comida = db.session.query(ComidaModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(comida, key, value)
        try:
            db.session.add(comida)
            db.session.commit()
            return comida.to_json(), 201
        except:
            return '', 404
        
    @role_required(roles=["Admin","Restaurante"])
    def delete(self, id):
        comida = db.session.query(ComidaModel).get_or_404(id)
        try:
            db.session.delete(comida)
            db.session.commit()
        except:
            return '', 404



class Comidas(Resource):
    @role_required(roles=["Admin"])
    def get(self):
        comidas = db.session.query(ComidaModel).all()
        return jsonify({
            'Comidas': [comida.to_json() for comida in comidas]
        })
    
    @role_required(roles=["Admin","Restaurante"])
    def post(self):
        comida = ComidaModel.from_json(request.get_json())
        db.session.add(comida)
        db.session.commit()
        return comida.to_json(), 201


