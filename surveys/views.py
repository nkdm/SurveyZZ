# Create your views here.
from django.http import HttpResponse
from surveys.models import Survey, PossibleAnswer, Vote
from django.template import loader, Context, RequestContext
from django.shortcuts import render, render_to_response

def index(request):
    allSurveys = Survey.objects.all()
    context = RequestContext(request, {
        "surveys": allSurveys,
    })
    template = loader.get_template("surveys/index.html")
    return HttpResponse(template.render(context))

def presentSurvey(request,id):
    if request.method=="GET":
        survey = Survey.objects.get(id=id)
        answers = PossibleAnswer.objects.filter(survey=survey)
        context = RequestContext( request, {
            "question": survey.question,
            "answers": answers
            })
        return render(request, "surveys/present.html", context)
    else:
        optionId = request.POST["answer"]
        answer = PossibleAnswer.objects.get(id = optionId)
        vote = Vote.objects.create(choice = answer)
        vote.save()
        context = Context ({ "answer" : answer  })
        return render(request, "surveys/thanks.html", context )

from django.db.models import Count
def results(request,id):
    survey  = Survey.objects.get(id=id)
    votes = PossibleAnswer.objects.filter(survey=survey).annotate( c= Count('vote'))
    context = Context({
            "votes": votes
    })
    return render(request, "surveys/results.html", context)

def login(request):
    return render(request, "surveys/login.html")
    
