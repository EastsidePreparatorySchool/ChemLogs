from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Q

from .models import Chemical, Transaction
from .forms import TransactionEditForm
from .forms import TransactionCreateForm


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     #template = loader.get_template('chemlogs/index.html')
#     #return HttpResponse(template.render(context, request))
#     return render(request, 'chemlogs/index.html', context) # this is a shorthand for the above two lines

# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     question = get_object_or_404(Question, pk=question_id) # shorthand for above
#     return render(request, 'chemlogs/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'chemlogs/results.html', {'question': question})

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'chemlogs/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('chemlogs:results', args=(question.id,)))

def testPage(request, chemical_id):
    chemical = get_object_or_404(Chemical, pk=chemical_id)
    return render(request, 'chemlogs/testPage.html', {'chemical': chemical})

def testPage2(request, chemical_id):
    chemical = get_object_or_404(Chemical, pk=chemical_id)
    if request.method == 'POST':
        form = TransactionCreateForm(request.POST)
        if form.is_valid():
            t = Transaction()
            t.amount = form.cleaned_data['amount']
            t.save()
            # some kind of confirmation ("you have added/removed this much")
    else:
        form = TransactionCreateForm()
    return render(request, 'chemlogs/testPage2.html', {'chemical': chemical, 'form': form})

def testChem(request, chemical_id):
    chemical = get_object_or_404(Chemical, pk=chemical_id)
    return render(request, 'chemlogs/testChem.html', {'chemical': chemical})

def chemical(request, chemical_id):
    chemical = get_object_or_404(Chemical, pk=chemical_id)
    return render(request, 'chemlogs/chemical.html', {'chemical': chemical})

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

def history(request):
    pass
    # will make this overall history page later

class ChemicalSearch(ListView):
    model = Chemical
    template_name = 'chemlogs/chemicalSearch.html'
    def get_queryset(self):
        nameSearch = self.request.GET.get("name")
        requireSomeInStock = self.request.GET.get("requireSomeInStock")

        toDisplay = Chemical.objects.all()
        if nameSearch:
            toDisplay = toDisplay.filter(name__icontains=nameSearch)
        if requireSomeInStock:
            toDisplay = filter(ChemicalSearch.inStock, toDisplay)
        return toDisplay
    
    def inStock(chemical):
        return chemical.computeAmount() > 0