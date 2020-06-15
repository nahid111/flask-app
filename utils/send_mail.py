import os
import smtplib
from email.mime.text import MIMEText


def send_mail(receiver, subject, message):

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['From'] = os.getenv('MAIL_DEFAULT_SENDER')
    msg['To'] = receiver

    # Send email
    with smtplib.SMTP(os.getenv('MAIL_SERVER'), os.getenv('MAIL_PORT')) as server:
        server.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
        server.sendmail(os.getenv('MAIL_DEFAULT_SENDER'), receiver, msg.as_string())
