from django import forms
from .models import Container, ChemicalState

class TransactionEditForm(forms.Form):
    type_choices = [ # N should not be an option
        ("T", "Standard (Add/Remove)"),
        ("R", "Reset (Override Container Amount)"),
        ("I", "Mistake (Transaction Will be Deleted)")
    ]

    amount = forms.IntegerField(max_value=9999, label="Amount")
    #type = forms.CharField(max_length=10, label="Type")
    type = forms.ChoiceField(choices=type_choices, label="Type")


class TransactionCreateForm(forms.Form):
    trSlide = forms.IntegerField(label="")

# set a new amount for a container
class ContainerOverrideForm(forms.Form):
    override_value = forms.IntegerField(label="New Amount")

class ContainerCreateForm(forms.Form):
    contents_choices = []
    def get_contents_choices(): # we need this function -- otherwise choices won't be dynamic
        return ContainerCreateForm.contents_choices

    initial_value = forms.IntegerField(label="Bottle Size")
    contents = forms.ChoiceField(choices=get_contents_choices, label="Chemical State")
    molarity = forms.FloatField(label="Molarity (M), if applicable", required=False)
    loc = forms.ChoiceField(choices=Container.LOC_CHOICES)
    # these *should ideally* only appear if contents is selected as "new state":
    state = forms.ChoiceField(label="Physical State", choices=ChemicalState.STATE_CHOICES, required=False)
    type = forms.CharField(label="Type", max_length=40, required=False)
    min_thresh = forms.IntegerField(label="Alert Threshold", required=False)

class ChemicalCreateForm(forms.Form):
    cas = forms.CharField(label="CAS") 
    safety = forms.CharField(label="Safety Link", required=False)

class SignInForm(forms.Form): # can also be used to create a user (sign up)
    email = forms.EmailField(label="Email")
    password = forms.PasswordInput()