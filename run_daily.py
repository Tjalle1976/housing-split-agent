import os
import smtplib
from email.mime.text import MIMEText

print("Housing split agent started")

smtp_host = os.environ["SMTP_HOST"]
smtp_port = int(os.environ["SMTP_PORT"])
smtp_user = os.environ["SMTP_USER"]
smtp_password = os.environ["SMTP_PASSWORD"]
email_to = os.environ["EMAIL_TO"]

subject = "Housing split agent test"
body = "De housing split agent draait succesvol op Render."

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = smtp_user
msg["To"] = email_to

server = smtplib.SMTP(smtp_host, smtp_port)
server.starttls()
server.login(smtp_user, smtp_password)
server.sendmail(smtp_user, email_to, msg.as_string())
server.quit()

print("Test email sent successfully")

