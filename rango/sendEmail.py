from email.mime.text import MIMEText
from datetime import date
import smtplib

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# Add your credentials here
SMTP_USERNAME = "showsalert26"
SMTP_PASSWORD = "megashow"

EMAIL_FROM = "showsalert26@gmail.com"
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
