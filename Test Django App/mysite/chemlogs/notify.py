# send email notifications

import smtplib
from email.message import EmailMessage
from django.contrib.auth import get_user_model
from email.mime.text import MIMEText

def job():
    from .models import ChemicalState
    low_states = [state for state in ChemicalState.objects.all() if state.needMore()]

    sender = "epschemlogs@gmail.com"
    password = "fjriypmcuywcnwyp" # warning: do not disclose this password
    s = smtplib.SMTP('smtp.gmail.com', 587) # used to be 587 or 25
    s.starttls()
    s.login(sender, password)

    User = get_user_model()
    for user in User.objects.all():
        send_email(s, sender, user, low_states)
    
    s.quit()

def send_email(s, sender, user, low_states):
    content = "Hello "
    content += user.username
    content += ",<br>Here is an automated snapshot of the EPS chemistry supply."
    content += "<br><br>Low chemical states:"
    for state in low_states:
        content += state.getNotification()
    content += "<br><br>Want to stop receiving notifications? <a href='localhost:8000/chemlogs/delete_account/"
    content += str(user.pk)
    content += "'>Delete account</a>"
    
    # message to be sent
    message = MIMEText(content, 'html')
    message['Subject'] = "ChemLogs Quarterly Update"
    message['From'] = sender
    message['To'] = "stippett@eastsideprep.org" # change this to user.username when not in development

    s.send_message(message)