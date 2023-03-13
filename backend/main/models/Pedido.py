from .. import db

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    clienteId = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    cliente = db.relationship("Cliente", back_populates="pedido", uselist=False, single_parent=True)
    restauranteId = db.Column(db.Integer, db.ForeignKey("restaurante.id"), nullable=False)
    restaurante = db.relationship("Restaurante", back_populates="pedido", uselist=False, single_parent=True)
    comidaId = db.Column(db.Integer, db.ForeignKey("comida.id"), nullable=False)
    comida = db.relationship("Comida", back_populates="pedido", uselist=False, single_parent=True)


    def __repr__(self):
            return f'Pedido: {self.id}'

    def to_json(self):
            pedido_json = {
                'id': self.id,
                'cliente': self.cliente.to_json(),
                'restaurante': self.restaurante.to_json(),
                'comida': self.comida.to_json(),


            }
            return pedido_json

    @staticmethod
    def from_json(pedido_json):
            id = pedido_json.get('id')
            clienteId = pedido_json.get('clienteId')
            restauranteId = pedido_json.get('restauranteId')
            comidaId = pedido_json.get('comidaId')
            return Pedido (
                id = id,
                clienteId = clienteId,
                restauranteId = restauranteId,
                comidaId = comidaId
            )



