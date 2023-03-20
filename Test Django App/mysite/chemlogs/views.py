from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Q
from django.utils import timezone
from .models import Chemical, Transaction, TransactionEdit, Container
from .forms import TransactionEditForm, TransactionCreateForm, ContainerOverrideForm, ContainerCreateForm
import itertools


# unused
def testPage(request, chemical_id):
    chemical = get_object_or_404(Chemical, pk=chemical_id)
    return render(request, 'chemlogs/testPage.html', {'chemical': chemical})

# main page for a chemical
def chemical(request, chemical_id):
    chemical = get_object_or_404(Chemical, pk=chemical_id)
    container_create_form = None
    if request.method == 'POST':
        container_create_form = ContainerCreateForm(request.POST)
        if container_create_form.is_valid():
            if container_create_form.cleaned_data['contents'] == "N":
                # create a new state for this new container
                chemical_state = chemical.chemicalstate_set.create(
                    state=container_create_form.cleaned_data['state'],
                    type=container_create_form.cleaned_data['type'],
                    min_thresh=container_create_form.cleaned_data['min_thresh']
                )
                # TODO: what if user tries to make a state that's equivalent to a preexisting state
            else:
                # find chemicalstate from form's 'contents' field, which stores either state or type.
                # state_list will either be empty or have 1 entry which is the chemicalstate
                # try to find chemicalstate from state
                state_list = chemical.chemicalstate_set.filter(
                    state=container_create_form.cleaned_data['contents']
                )
                if len(state_list) == 0: # can you just say !chemical_state?
                    # override state_list, finding from type
                    state_list = chemical.chemicalstate_set.filter(
                        type=container_create_form.cleaned_data['contents']
                    )
                chemical_state = state_list[0]

            # give the bottle an id.
            # look through AA, AB, ..., AZ, BA, ..., ZZ until you find an unused id
            start = ord("A")
            alphabet_length = 26
            end = start + alphabet_length
            letters_ascii = range(start, end)
            bad_ids = [ # no container should have an id from this list
                # confusion with aqueous
                "AQ",
                # confusion with location
                "MS", "US",
                # confusion with chemical formula
                "HF", "HI", "KH", "KF", "KI"
            ]
            for i, j in itertools.product(letters_ascii, letters_ascii): # this avoids nested for loops
                potential_id = chr(i) + chr(j)
                if len(Container.objects.filter(id=potential_id)) == 0 and potential_id not in bad_ids:
                    container_id = potential_id
                    break
            
            new_container = chemical_state.container_set.create(
                initial_value=container_create_form.cleaned_data['initial_value'],
                contents=container_create_form.cleaned_data['contents'],
                loc=container_create_form.cleaned_data['loc'],
                id=container_id
            )
            if container_create_form.cleaned_data['molarity']:
                new_container.molarity = container_create_form.cleaned_data['molarity']
                new_container.save() # i think that's necessary but haven't tested without it
            # create an N transaction
            new_container.transaction_set.create(
                type="N",
                amount=container_create_form.cleaned_data['initial_value'],
                time=timezone.now()
            )
    if not container_create_form:
        ContainerCreateForm.contents_choices = [
            ("N", "Add New")
        ]
        for state in chemical.chemicalstate_set.all():
            if not state.type:
                to_append = state.state
            else:
                to_append = state.type
            ContainerCreateForm.contents_choices.append((to_append, to_append))
        container_create_form = ContainerCreateForm()
    return render(request, 'chemlogs/chemical.html', {'chemical': chemical, 'container_create_form': container_create_form})

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
            new_amount = edit_form.cleaned_data['amount']
            new_type = edit_form.cleaned_data['type']
            # record the change
            edit = transaction.transactionedit_set.create(
                date=timezone.now(),
                old_amount=transaction.amount,
                new_amount=new_amount,
                old_type=transaction.type,
                new_type=new_type
            )

            # make the change
            transaction.amount = new_amount
            transaction.type = new_type
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
                container.transaction_set.create(amount=transact_form.cleaned_data['trSlide'], time=timezone.now(), type="T")
                # some kind of confirmation ("you have added/removed this much")
        elif "transact_remove" in request.POST:
            transact_form = TransactionCreateForm(request.POST, auto_id='%s')
            if transact_form.is_valid():
                value = 0 - transact_form.cleaned_data['trSlide']
                container.transaction_set.create(amount=value, time=timezone.now(), type="T")
                # add confirmation
        elif "override" in request.POST:
            override_form = ContainerOverrideForm(request.POST, auto_id='%s')
            if override_form.is_valid():
                container.transaction_set.create(amount=override_form.cleaned_data['override_value'], time=timezone.now(), type="R")
                # add confirmation
    if not transact_form:
        transact_form = TransactionCreateForm(auto_id='%s') # this argument makes the input's id "trSlide" rather than "id_trSlide"
    if not override_form:
        override_form = ContainerOverrideForm()
    return render(request, 'chemlogs/container.html', {'container': container, 'transact_form': transact_form, 'override_form': override_form})

# unimplemented
def history(request):
    #return render(request, 'chemlogs/history.html', {'actions': Transaction.objects.exclude(type="I").order_by('-time')})
    pass

# search for chemicals
class ChemicalSearch(ListView):
    model = Chemical
    template_name = 'chemlogs/chemicalSearch.html'

    def get_context_data(self):
        shown_chemicals = self.get_queryset()
        filtered = len(shown_chemicals) < len(Chemical.objects.all()) # whether some chemicals are excluded in search
        actions = Transaction.objects.exclude(type="I").order_by('-time')
        return {'shown_chemicals': shown_chemicals, 'filtered': filtered, 'actions': actions}

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