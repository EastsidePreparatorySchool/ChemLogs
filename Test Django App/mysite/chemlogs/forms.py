from django import forms

class TransactionEditForm(forms.Form):
    amount = forms.IntegerField(label="Amount")
    type = forms.CharField(max_length=10, label="Type")

class TransactionCreateForm(forms.Form):
    trSlide = forms.IntegerField(label="")

# set a new amount for a container
class ContainerOverrideForm(forms.Form):
    override_value = forms.IntegerField(label="New Amount")