from django.contrib import admin

# Register your models here.

from .models import Question, Choice, Chemical, Transaction

#admin.site.register(Question)
#admin.site.register(Choice)
admin.site.register(Chemical)
admin.site.register(Transaction)