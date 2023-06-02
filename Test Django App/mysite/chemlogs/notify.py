# send email notifications

import smtplib
from email.message import EmailMessage
from django.contrib.auth import get_user_model

def job():
    from .models import ChemicalState
    low_states = [state for state in ChemicalState.objects.all() if state.needMore()]
    send_email("dlao@eastsideprep.org", low_states)

def send_email(address, low_states):
    content = "Hello users of chemLogs,\nHere is an automated snapshot of the chemistry supply."
    content += "\n\nLow chemical states:"
    for state in low_states:
        content += state.getNotification()
    
    sender = "epschemlogs@gmail.com"
    password = "fjriypmcuywcnwyp" # warning: do not disclose this password
    User = get_user_model()
    receiver_addresses = [user.email for user in User.objects.all()]
    
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(sender, password)

    # message to be sent
    message = EmailMessage()
    message.set_content(content)
    message['Subject'] = "ChemLogs Quarterly Update"
    message['From'] = sender
    message['To'] = receiver_addresses

    s.send_message(message)
    s.quit()