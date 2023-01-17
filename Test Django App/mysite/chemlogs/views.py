from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Q
import datetime

from .models import Chemical, Transaction, Container
from .forms import TransactionEditForm
from .forms import TransactionCreateForm

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
    if request.method == 'POST':
        form = TransactionEditForm(request.POST)
        if form.is_valid():
            transaction.amount = form.cleaned_data['amount']
            transaction.save()
            # there should be a confirmation "are you sure?"
    else:
        form = TransactionEditForm(initial={'amount': transaction.amount})
    return render(request, 'chemlogs/transaction.html', {'transaction': transaction, 'form': form})

def container(request, container_id):
    container = get_object_or_404(Container, pk=container_id)
    if request.method == 'POST':
        form = TransactionCreateForm(request.POST, auto_id='%s')
        if form.is_valid():
            container.transaction_set.create(amount=form.cleaned_data['trSlide'], time=datetime.datetime.now())
            # some kind of confirmation ("you have added/removed this much")
    else:
        form = TransactionCreateForm(auto_id='%s') # this argument makes the input's id "trSlide" rather than "id_trSlide"
    return render(request, 'chemlogs/container.html', {'container': container, 'form': form})

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