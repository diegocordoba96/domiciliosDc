from flask import request, Blueprint
from .. import db 
from main.models import ClienteModel
from flask_jwt_extended import create_access_token
from main.auth.decorators import user_identity_lookup
from main.mail.function import send_mail

auth = Blueprint('auth', __name__, url_prefix='/auth')



@auth.route('/login', methods=['POST'])
def loggin():
    cliente = db.session.query(ClienteModel).filter(ClienteModel.correo == request.get_json().get('correo')).first_or_404()


    if cliente.validate_pass(request.get_json().get('password')):
        access_token = create_access_token(identity=cliente)
         
        data = {
            'id': str(cliente.id),
            'correo': cliente.correo,
            'acces_token': access_token,
            'rol': str(cliente.rol)
        }

        return data, 200
    else:
        return 'Password invalid',401
 

@auth.route('/register',  methods=['POST'])
def register():
    cliente = ClienteModel.from_json(request.get_json())
    exits = db.session.query(ClienteModel).filter(ClienteModel.correo == cliente.correo).scalar() is not None 

    if exits:
        return 'Duplicated email',409
    else:
        try:
            db.session.add(cliente)
            db.session.commit()
            send_mail([cliente.correo], "Bienvenido", 'register', cliente = cliente)
        except Exception as error:
            db.session.rollback()
            return str(error), 409
        return cliente.to_json(),201