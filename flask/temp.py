import smtplib
from email.message import EmailMessage

def email_alert(subject, to, numPeople):
    msg = EmailMessage()
    msg.set_content("A fire has been dected with " + str(numPeople) + " people around!")
    msg['subject'] = subject
    msg['to'] = to

    user = "flameainotifications@gmail.com"
    msg['from'] = user
    password = "mfdcailizcqtyyim"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()

email_alert("Fire Alert Test", "2403709017@txt.att.net", 3)
email_alert("Fire Alert Test", "saraanshwadkar@gmail.com", 2)