from django.contrib import admin

# Register your models here.

from .models import Chemical, Transaction, Container, ChemicalState

admin.site.register(Chemical)
admin.site.register(Transaction)
admin.site.register(Container)
admin.site.register(ChemicalState)