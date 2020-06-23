from app import make_celery
from utils.send_mail import send_mail

celery = make_celery()


# ======================================================================================
#                                   Sending E-mails
# ======================================================================================
@celery.task(name='tasks.send_mail_task')
def send_mail_task(receiver, subject, message):
    """
    Send an e-mail.

    :param receiver: E-mail address of the visitor
    :type receiver: str
    :param subject: Subject of the E-mail
    :type receiver: str
    :param message: E-mail message
    :type message: str
    :return: None
    """

    send_mail(receiver, subject, message)

    return None
