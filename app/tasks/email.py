from flask_mail import Message
from app.extensions import mail, celery

@celery.task
def send_async_email(email_data):
    msg = Message(email_data['subject'],
                  recipients=email_data['to'],
                  body=email_data['body'])
    mail.send(msg)