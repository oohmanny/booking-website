from flask import render_template
from flask_mail import Message, Mail

mail = Mail()

@staticmethod
def invia_mail(oggetto='', destinatario='', template='', prenotazione='', link=''):
    msg = Message(oggetto + " - Autoriparazioni San Bernardo", [destinatario])
    msg.html = render_template(template, **prenotazione, link=link)
    mail.send(msg)