from .. import db
import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash


class Cliente(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(45), nullable=False)
    correo = db.Column(db.String(60), nullable=False, unique=True, index=True)
    telefono = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(60), nullable=False)
    rol = db.Column(db.String(45), nullable=False, default='Cliente')
    fecha_registro = db.Column(db.DateTime(45), default=dt.datetime.now(), nullable=False)
    pedido = db.relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")



    @property
    def plain_password(self):
        raise AttributeError()
    
    @plain_password.setter
    def plain_password(self,password):
        self.password = generate_password_hash(password)


    def validate_pass(self, password):
        return check_password_hash(self.password, password)



    def __repr__(self):
        return f'{self.nombre}'

    def to_json(self):
        cliente_json = {
            'id': self.id,
            'nombre': self.nombre,
            'correo': self.correo,
            'telefono': self.telefono,
            'direccion': self.direccion, 
            'rol': self.rol,
            'fecha_registro': str(self.fecha_registro)
        }
        return cliente_json

    @staticmethod
    def from_json(cliente_json):
        id = cliente_json.get('id')
        nombre = cliente_json.get('nombre')
        correo = cliente_json.get('correo')
        telefono = cliente_json.get('telefono')
        password = cliente_json.get('password')
        direccion = cliente_json.get('direccion')
        rol = cliente_json.get('rol')
        fecha_registro = cliente_json.get('fecha_registro')
        return Cliente(
            id = id,
            nombre = nombre,
            correo = correo,
            telefono = telefono,
            plain_password = password,
            direccion = direccion,
            rol = rol,
            fecha_registro = fecha_registro
        )



