from ..import jwt
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def role_required(roles):
    def decorator(funcion):
        def wrapper(*args, **kwargs):
            #Verificar que JWT es correcto
            verify_jwt_in_request()
            #Obtenemos los claims(peticiones), que están dentro del 
            claims = get_jwt()
            if claims['sub']['role'] in roles:
                return funcion(*args,**kwargs)
            else:
                return 'Rol not allowed',403
        return wrapper
    return decorator



#decoradores existentes, redefinidos
@jwt.user_identity_loader
def user_identity_lookup(cliente):
    return {
        'clienteId': cliente.id,
        'role': cliente.rol

    }


@jwt.additional_claims_loader
def add_claims_to_access_token(cliente):
    claims = {
        'id': cliente.id,
        'rol': cliente.rol,
        'correo': cliente.correo
    }

