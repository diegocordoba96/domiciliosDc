from flask_restful import Resource
from flask import jsonify, request
from .. import db
from main.models import ClienteModel
from main.auth.decorators import role_required
from flask_jwt_extended import get_jwt_identity


class Cliente(Resource):

    @role_required(roles=['Admin', "Cliente"])
    def get(self, id):
        cliente = db.session.query(ClienteModel).get_or_404(id)
        current_user = get_jwt_identity()
        if cliente.rol == 'Cliente':
            if current_user['clienteId'] == cliente.id or current_user['role'] == 'Admin':
                return cliente.to_json()
            else:
                return 'Unauthorized',401
        else:
            return 'Resource not found', 404

    @role_required(roles=["Cliente"])
    def put(self, id):
        cliente = db.session.query(ClienteModel).get_or_404(id)
        current_user = get_jwt_identity()
        if cliente.rol == 'Cliente' and current_user == cliente.id:
            data = request.get_json().items()
            for key, value in data:
                setattr(cliente, key, value)
            try:
                db.session.add(cliente)
                db.session.commit()
                return cliente.to_json(), 201
            except:
                return '', 404
        else:
            return 'Unauthorized',401

    @role_required(roles=["Cliente"])
    def delete(self, id):
        cliente = db.session.query(ClienteModel).get_or_404(id)
        current_user = get_jwt_identity()
        if cliente.rol == 'Cliente' and current_user == cliente.id:
            try:
                db.session.delete(cliente)
                db.session.commit()
            except:
                return '', 404
        else:
                return 'Unauthorized',401


class Clientes(Resource):
    @role_required(roles=['Admin'])
    def get(self):
        clientes = db.session.query(ClienteModel).all()
        return jsonify({
            'Clientes': [cliente.to_json() for cliente in clientes]
        })

    def post(self):
        cliente = ClienteModel.from_json(request.get_json())
        db.session.add(cliente)
        db.session.commit()
        return cliente.to_json(), 201