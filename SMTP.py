import smtplib
from email.mime.text import MIMEText


class SMTP:
    sender = None
    password = None
    receivers = None

    def __init__(self, _sender, _password, _receivers):
        self.sender = _sender
        self.password = _password
        self.receivers = _receivers

    def send_email_message(self, subject, message):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = ", ".join(self.receivers)

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(self.sender, self.password);
        smtp.send_message(msg)
        smtp.close()