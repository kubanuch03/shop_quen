from django.core.mail import send_mail
from config.celery import app


@app.task(bind=True)
def reset_password(self, email):
    subject = "Enagro"
    message = "Вам пришли новые уведемления"

    from_email = "sadyr.top@gmail.com"
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=True)

    return "Done"