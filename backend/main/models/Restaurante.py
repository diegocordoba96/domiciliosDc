from .. import db

class Restaurante(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(55), nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.String(60), nullable=False)
    comidas = db.relationship("Comida", back_populates="restaurantes", uselist=False,  cascade="all, delete-orphan")
    pedido = db.relationship("Pedido", back_populates="restaurante", cascade="all, delete-orphan")



    def __repr__(self):
        return f'Restaurante: {self.nombre}'

    def to_json(self):
        restaurante_json = {
            'id': self.id,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'direccion': self.direccion 
        }
        return restaurante_json

    @staticmethod
    def from_json(restaurante_json):
        id = restaurante_json.get('id')
        nombre = restaurante_json.get('nombre')
        telefono = restaurante_json.get('telefono')
        direccion = restaurante_json.get('direccion')
        return Restaurante(
            id = id,
            nombre = nombre,
            telefono = telefono,
            direccion = direccion,
        )



