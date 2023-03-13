import os
from flask import Flask
from dotenv import load_dotenv


#import modulo para crear api-rest
from flask_restful import Api

#importación de modulo para conectarme con DB
from flask_sqlalchemy import SQLAlchemy

#importación modulo JWT
from flask_jwt_extended import JWTManager

#Importación de modulos para envios de correo
from flask_mail import Mail 

api = Api()
db = SQLAlchemy()
jwt = JWTManager()
mailsender = Mail()


def create_app():
    app = Flask(__name__)

    #cargar variables de entron
    load_dotenv()

    #configuración base de datos
    PATH = os.getenv("DATABASE_PATH")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    if not os.path.exists(f'{PATH}{DATABASE_NAME}'):
        os.chdir(f'{PATH}')
        file = os.open(f'{DATABASE_NAME}', os.O_CREAT)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PATH}{DATABASE_NAME}'
    db.init_app(app)


    import main.resources as resources

    #api.add_resource(resources.clientesViejoResource, '/clientesviejo')
    #api.add_resource(resources.clienteViejoResource, '/clientesviejo/<id>')
    api.add_resource(resources.ClientesResource, '/clientes/')
    api.add_resource(resources.ClienteResource, '/cliente/<id>')
    api.add_resource(resources.ComidasResource, '/comidas/')
    api.add_resource(resources.ComidaResource, '/comida/<id>')
    api.add_resource(resources.RestaurantesResource, '/restaurantes/')
    api.add_resource(resources.RestauranteResource, '/restaurante/<id>')
    api.add_resource(resources.PedidosResource, '/pedidos/')
    api.add_resource(resources.PedidoResource, '/pedido/<id>')




    api.init_app(app)

    #Configurando JWT
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES"))
    jwt.init_app(app)

    #Blueprint
    from main.auth import routes
    app.register_blueprint(auth.routes.auth)
    
    from main.mail import function
    app.register_blueprint(mail.function.mail)



    #Configurar Mail
    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_FLASKY_MAIL_SENDER'] = os.getenv('MAIL_FLASKY_MAIL_SENDER')

    mailsender.init_app(app)




    return app
