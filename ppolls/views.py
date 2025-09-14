from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.template import loader
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'ppolls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'ppolls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'ppolls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request,'ppolls/detail.html',
        {
            'question': question,
            "error_message": "You didn't select a choice.",
        },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("ppolls:results", args=(question.id,)))

