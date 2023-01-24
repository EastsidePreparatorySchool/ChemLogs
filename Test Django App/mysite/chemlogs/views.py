from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Q
import datetime

from .models import Chemical, Transaction, Container
from .forms import TransactionEditForm, TransactionCreateForm, ContainerOverrideForm

# unused
def testPage(request, chemical_id):
    chemical = get_object_or_404(Chemical, pk=chemical_id)
    return render(request, 'chemlogs/testPage.html', {'chemical': chemical})

# main page for a chemical
def chemical(request, chemical_id):
    chemical = get_object_or_404(Chemical, pk=chemical_id)
    return render(request, 'chemlogs/chemical.html', {'chemical': chemical})

def testChem(request, chemical_id):
    chemical = get_object_or_404(Chemical, pk=chemical_id)
    return render(request, 'chemlogs/testChem.html', {'chemical': chemical})

# view and modify a transaction
def transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    edit_form = None
    if request.method == 'POST':
        edit_form = TransactionEditForm(request.POST)
        if edit_form.is_valid():
            transaction.amount = edit_form.cleaned_data['amount']
            transaction.type = edit_form.cleaned_data['type']
            transaction.save()
            # there should be a confirmation "are you sure?"
    if not edit_form:
        edit_form = TransactionEditForm(initial={'amount': transaction.amount, 'type': transaction.type})
    return render(request, 'chemlogs/transaction.html', {'transaction': transaction, 'edit_form': edit_form})

def container(request, container_id):
    container = get_object_or_404(Container, pk=container_id)
    transact_form = None
    override_form = None
    if request.method == 'POST':
        if "transact_add" in request.POST:
            transact_form = TransactionCreateForm(request.POST, auto_id='%s')
            if transact_form.is_valid():
                container.transaction_set.create(amount=transact_form.cleaned_data['trSlide'], time=datetime.datetime.now(), type="T")
                # some kind of confirmation ("you have added/removed this much")
        elif "transact_remove" in request.POST:
            transact_form = TransactionCreateForm(request.POST, auto_id='%s')
            if transact_form.is_valid():
                value = 0 - transact_form.cleaned_data['trSlide']
                container.transaction_set.create(amount=value, time=datetime.datetime.now(), type="T")
                # add confirmation
        elif "override" in request.POST:
            override_form = ContainerOverrideForm(request.POST, auto_id='%s')
            if override_form.is_valid():
                container.transaction_set.create(amount=override_form.cleaned_data['override_value'], time=datetime.datetime.now(), type="R")
                # add confirmation
    if not transact_form:
        transact_form = TransactionCreateForm(auto_id='%s') # this argument makes the input's id "trSlide" rather than "id_trSlide"
    if not override_form:
        override_form = ContainerOverrideForm()
    return render(request, 'chemlogs/container.html', {'container': container, 'transact_form': transact_form, 'override_form': override_form})

# unimplemented
def history(request):
    pass
    # will make this overall history page later

# search for chemicals
class ChemicalSearch(ListView):
    model = Chemical
    template_name = 'chemlogs/chemicalSearch.html'
    def get_queryset(self):
        nameSearch = self.request.GET.get("name")
        requireSomeInStock = self.request.GET.get("requireSomeInStock")

        toDisplay = Chemical.objects.all()
        if nameSearch:
            # have to correct for formatting and want to filter by place but it works
            # https://docs.djangoproject.com/en/4.1/topics/db/queries/#complex-lookups-with-q
            # used the above for the OR query, since filter() can't handle it
            toDisplay = toDisplay.filter(Q(name__icontains=nameSearch) | 
                Q(formula__icontains=nameSearch))
        if requireSomeInStock:
            toDisplay = filter(ChemicalSearch.inStock, toDisplay)
        return toDisplay
    
    def inStock(chemical):
        return chemical.computeAmount() > 0