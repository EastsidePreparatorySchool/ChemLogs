from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse

from .models import Choice, Question, Chemical

# Create your views here.


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    #template = loader.get_template('chemlogs/index.html')
    #return HttpResponse(template.render(context, request))
    return render(request, 'chemlogs/index.html', context) # this is a shorthand for the above two lines

def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    question = get_object_or_404(Question, pk=question_id) # shorthand for above
    return render(request, 'chemlogs/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'chemlogs/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'chemlogs/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('chemlogs:results', args=(question.id,)))

def testPage(request, chemical_id):
    chemical = get_object_or_404(Chemical, pk=chemical_id)
    return render(request, 'chemlogs/testPage.html', {'chemical': chemical})

def testPage2(request, chemical_id):
    chemical = get_object_or_404(Chemical, pk=chemical_id)
    return render(request, 'chemlogs/testPage2.html', {'chemical': chemical})

def testChem(request, chemical_id):
    chemical = get_object_or_404(Chemical, pk=chemical_id)
    return render(request, 'chemlogs/testChem.html', {'chemical': chemical})

def chemical(request, chemical_id):
    chemical = get_object_or_404(Chemical, pk=chemical_id)
    return render(request, 'chemlogs/chemical.html', {'chemical': chemical})