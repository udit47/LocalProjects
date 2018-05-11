# all imports
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from .models import Question,Choice
from django.urls import reverse
from django.views import generic

# Indexview class using generic listview for getting latest questions
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Return last 5 published questions
        return Question.objects.order_by('-pub.date')[:5]

# DetailView class using generic DetailView for getting details of particular question
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

# Resultview class using generic DetailView for viewing results of polls of a question
class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# Vote view for voting on a particular question.
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question' : question,
            'error_message' : 'You did not select a choice. Please select one.'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
