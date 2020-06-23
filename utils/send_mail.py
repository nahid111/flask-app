from os import getenv
import smtplib
from email.mime.text import MIMEText


def send_mail(receiver, subject, message):

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['From'] = getenv('MAIL_DEFAULT_SENDER')
    msg['To'] = receiver

    # Send email
    with smtplib.SMTP(getenv('MAIL_SERVER'), getenv('MAIL_PORT')) as server:
        server.login(getenv('MAIL_USERNAME'), getenv('MAIL_PASSWORD'))
        server.sendmail(getenv('MAIL_DEFAULT_SENDER'), receiver, msg.as_string())
