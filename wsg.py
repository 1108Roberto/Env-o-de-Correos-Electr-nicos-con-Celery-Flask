# app.py

from flask import Flask
from celery import Celery

app = Flask(__name__)
app.config.from_object('celeryconfig')

celery = Celery(app.name, broker=app.config['broker_url'])
celery.conf.update(app.config)

# app.py (continuación)

from flask_mail import Mail, Message

mail = Mail(app)

@celery.task
def send_email(subject, sender, recipients, body):
    with app.app_context():
        msg = Message(subject, sender=sender, recipients=[recipients])
        msg.body = body
        mail.send(msg)

# app.py (continuación)

from tasks import send_email  # Asegúrate de ajustar el import según tu estructura de carpetas

@app.route('/enviar_correo', methods=['POST'])
def enviar_correo():
    # Lógica para obtener los datos del formulario
    subject = request.form['subject']
    sender = 'your-email@example.com'  # Puede ser una dirección de correo configurada
    recipients = request.form['recipient']
    body = request.form['body']

    # Llamar a la tarea Celery para enviar el correo electrónico de manera asíncrona
    send_email.delay(subject, sender, recipients, body)

    # Lógica adicional de respuesta
    return 'Correo en proceso de envío.'

