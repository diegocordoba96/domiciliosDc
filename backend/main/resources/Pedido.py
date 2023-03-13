from flask_restful import Resource
from flask import jsonify, request
from .. import db
from main.models import PedidoModel
from main.auth.decorators import role_required
from flask_jwt_extended import get_jwt_identity



class Pedido(Resource):
    @role_required(roles=['Admin', 'Cliente'])
    def get(self, id):
        pedido = db.session.query(PedidoModel).get_or_404(id)
        current_user = get_jwt_identity()
        if current_user['clienteId'] == pedido.clienteId or current_user['role'] == 'Admin':
            try:
                return pedido.to_json()
            except:
                return 'Resource not found', 404
    @role_required(roles=['Admin'])
    def put(self, id):
        pedido = db.session.query(PedidoModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(pedido, key, value)
        try:
            db.session.add(pedido)
            db.session.commit()
            return pedido.to_json(), 201
        except:
            return '', 404
    @role_required(roles=['Admin'])
    def delete(self, id):
        restaurante = db.session.query(PedidoModel).get_or_404(id)
        try:
            db.session.delete(restaurante)
            db.session.commit()
        except:
            return '', 404



class Pedidos(Resource):
    @role_required(roles=['Admin'])
    def get(self):
        pedidos = db.session.query(PedidoModel).all()
        return jsonify({
            'Pedidos': [pedido.to_json() for pedido in pedidos]
        })

    @role_required(roles=['Admin','Cliente'])
    def post(self):
        pedido = PedidoModel.from_json(request.get_json())
        db.session.add(pedido)
        db.session.commit()
        return pedido.to_json(), 201

