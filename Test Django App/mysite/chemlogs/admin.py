from django.contrib import admin

# Register your models here.

from .models import Chemical, Transaction, Bottle, ChemicalState

admin.site.register(Chemical)
admin.site.register(Transaction)
admin.site.register(Bottle)
admin.site.register(ChemicalState)