from django import forms
from django.core.validators import RegexValidator
from .models import Container, ChemicalState

class TransactionEditForm(forms.Form):
    type_choices = [ # N should not be an option
        ("T", "Standard (Add/Remove)"),
        ("R", "Reset (Override Container Amount)"),
        ("I", "Mistake (Transaction will be Deleted)")
    ]

    type = forms.ChoiceField(choices=type_choices, label="Type")
    amount = forms.IntegerField(max_value=9999, label="Amount")


class TransactionCreateForm(forms.Form):
    new_amount = forms.FloatField(label="")

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
    min_thresh = forms.IntegerField(label="Alert Threshold (g)", required=False)

class StateEditForm(forms.Form):
    # these are all the same as the last three lines of ContainerCreateForm (above). Could possibly
    # just delete those three lines and use both forms maybe.
    state = forms.ChoiceField(label="Physical State", choices=ChemicalState.STATE_CHOICES, required=False)
    type = forms.CharField(label="Type", max_length=40, required=False)
    min_thresh = forms.IntegerField(label="Alert Threshold (g)", required=False)

class ChemicalCreateForm(forms.Form):
    name = forms.CharField(label="Chemical Name")
    cas = forms.CharField(label="CAS") 
    formula = forms.CharField(label="Formula")
    safety = forms.CharField(label="SDS Link", required=False)
    molar_mass = forms.FloatField(label="Molar Mass (g)", required=False)
    dangerous = forms.BooleanField(label="Potentially Dangerous?", required=False)

class SignInForm(forms.Form): # can also be used to create a user (sign up) (is this used?)
    email = forms.EmailField(label="Email")
    password = forms.PasswordInput()

# the form to jump to a container page. Used in chemicalSearch page.
class GoToContainerForm(forms.Form):
    # container id
    container = forms.CharField(max_length=2, min_length=2, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Enter ID'} # this text displays when input is empty
    ))