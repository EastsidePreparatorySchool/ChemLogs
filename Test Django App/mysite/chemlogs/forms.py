from django import forms

class TransactionEditForm(forms.Form):
    amount = forms.IntegerField(label="Amount")

class TransactionCreateForm(forms.Form):
    trSlide = forms.IntegerField(label="")