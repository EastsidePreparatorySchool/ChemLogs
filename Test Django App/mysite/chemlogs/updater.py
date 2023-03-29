# from https://medium.com/@kevin.michael.horan/scheduling-tasks-in-django-with-the-advanced-python-scheduler-663f17e868e6

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from . import notify
import socket

def start():
    # the try-except fexes the problem of double-scheduling due to django reloading right after it loads initially. This is from:
    # https://stackoverflow.com/questions/16053364/make-sure-only-one-worker-launches-the-apscheduler-event-in-a-pyramid-web-app-ru/27303834#27303834
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 47200))
    except socket.error:
        # don't start scheduler because this is a reload
        pass
    else:
        # start scheduler
        scheduler = BackgroundScheduler()
        notify_job = {'month': '12,3,6', 'day': '1', 'hour': '8', 'minute': '0', 'second': '0'}
        scheduler.add_job(notify.job, 'cron', **notify_job)
        scheduler.start()