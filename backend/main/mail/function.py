from..import mailsender, db
from flask import current_app, render_template, Blueprint
from flask_mail import Message
from smtplib import SMTPException
from main.models import ClienteModel, RestauranteModel
from main.auth.decorators import role_required



def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, sender=current_app.config['MAIL_FLASKY_MAIL_SENDER'], recipients=to)
    try:
        msg.body = render_template(f'{template}.txt', **kwargs)
        mailsender.send(msg)
    except SMTPException as error:
        print('Mail deliver failed', error)
    return True


mail = Blueprint('mail', __name__, url_prefix='/mail')



@mail.route('/newsletter', methods=['POST'])
@role_required(roles=['Admin'])
def newsletter():
    clientes = db.session.query(ClienteModel).filter(ClienteModel.rol == 'Cliente').all()
    restaurantes = db.session.query(RestauranteModel).all()

    try:
        for cliente in clientes:
            send_mail([cliente.correo],"Restaurantes disponibles", 'newsletter',  cliente = cliente, restaurantes = [restaurante.nombre for restaurante in restaurantes])

    except SMTPException as error:
        return 'Mail deliver failed'
    return 'Mails Sent',200
