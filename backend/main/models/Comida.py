from .. import db

class Comida(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(55), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    restauranteId = db.Column(db.Integer, db.ForeignKey('restaurante.id'), nullable=False)
    restaurantes = db.relationship('Restaurante', back_populates="comidas", uselist=False)
    #restaurante = db.relationship('Restaurante', back_populates='comidas', cascade="all, delete-orphan")
    pedido = db.relationship("Pedido", back_populates="comida", cascade="all, delete-orphan")




    def __repr__(self):
        return f'Comida: {self.nombre}'

    def to_json(self):
        comida_json = {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'restaurante': self.restaurantes.to_json()
        }
        return comida_json

    @staticmethod
    def from_json(comida_json):
        id = comida_json.get('id')
        nombre = comida_json.get('nombre')
        precio = comida_json.get('precio')
        restauranteId = comida_json.get('restauranteId')
        return Comida (
            id = id,
            nombre = nombre,
            precio = precio,
            restauranteId = restauranteId
        )



