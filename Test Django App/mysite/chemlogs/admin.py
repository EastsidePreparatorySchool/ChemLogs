from django.contrib import admin

# Register your models here.

from .models import Chemical, Transaction

admin.site.register(Chemical)
admin.site.register(Transaction)