from django.apps import AppConfig

class ChemLogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chemlogs'
    def ready(self): # fromhttps://medium.com/@kevin.michael.horan/scheduling-tasks-in-django-with-the-advanced-python-scheduler-663f17e868e6
        from . import updater
        updater.start()