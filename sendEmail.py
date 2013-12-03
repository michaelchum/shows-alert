from email.mime.text import MIMEText
from datetime import date
import smtplib

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "uehtesham90@gmail.com"
SMTP_PASSWORD = "mutation1A"

EMAIL_FROM = "uehtesham90@gmail.com"
EMAIL_SPACE = ", "

def send_email(to, subject, link):
    text = link
    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['To'] = EMAIL_SPACE.join(to)
    msg['From'] = EMAIL_FROM
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, to, msg.as_string())
    mail.quit()

# if __name__=='__main__':
#     send_email()
to = ['usman.ehtesham@mail.mcgill.ca', 'uehtesham90@gmail.com']
send_email(to, 'hey fucker', 'here is the link to latest episode')