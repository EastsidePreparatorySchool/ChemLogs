# send email notifications

def job():
    from .models import ChemicalState
    low_states = [state for state in ChemicalState.objects.all() if state.needMore()]
    send_email("dlao@eastsideprep.org", low_states)

def send_email(address, low_states):
    print("Low chemical states:")
    for state in low_states:
        print(state.getNotification())