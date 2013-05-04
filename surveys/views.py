# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from surveys.models import Survey, PossibleAnswer, User, Questionnaire
from django.template import loader, Context, RequestContext
from django.shortcuts import render, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.forms.widgets import RadioSelect, Textarea
from django.forms.models import BaseModelFormSet, modelformset_factory

def index(request):
    allSurveys = Survey.objects.all()
    context = RequestContext(request, {
        "surveys": allSurveys,
    })
    template = loader.get_template("surveys/index.html")
    return HttpResponse(template.render(context))


from django import forms
from django.forms.widgets import RadioSelect

class SurveyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self,obj):
        return obj.text

class PresentSurveyForm(forms.Form):
    def __init__(self,survey=None, *args, **kwargs):
        super(PresentSurveyForm, self).__init__(*args, **kwargs)
        self.fields['text'] = SurveyModelChoiceField( queryset = PossibleAnswer.objects.filter(survey=survey) , 
                                                      widget = RadioSelect,
                                                      empty_label = None,
                                                      label =  survey.question if survey else ""
                                                      )

def presentSurvey(request, id):
    if request.method=="GET":
        survey = Survey.objects.get(id=id)
        try:
            currentAnswer = request.user.possibleanswer_set.get(survey=survey)
            form = PresentSurveyForm(survey, initial={'text': currentAnswer.id})
        except:
            form = PresentSurveyForm(survey)

        context = RequestContext( request, {
            "form": form
            })
        return render(request, "surveys/present.html", context)
    else:
        form = PresentSurveyForm(data = request.POST)
        optionId = form.data['text']
        answer = PossibleAnswer.objects.get(id = optionId)      
        request.user.possibleanswer_set = [answer]
        context = RequestContext(request,{
                'answer':answer
        })
        return render(request, "surveys/thanks.html", context )

from django.db.models import Count
def results(request,id):
    survey  = Survey.objects.get(id=id)
    votes = PossibleAnswer.objects.filter(survey=survey).annotate( c= Count('voters'))
    context = Context({
            "votes": votes,
            "question": survey.question
    })
    return render(request, "surveys/results.html", context)

def login(request, context=None):
    return render(request, "surveys/login.html")

def admin(request):
    if request.user.is_superuser:
        return HttpResponseRedirect("/admin-django")
    elif request.user.is_authenticated():
        return render(request, "registration/nopermission.html")
    else:
        return HttpResponseRedirect("/login?next=/admin")

def questionnaires(request):
    questionnaires = Questionnaire.objects.all()
    context = Context({
            "questionnaires": questionnaires
    })
    return render(request, "surveys/questionnaires.html", context)

class QuestionnaireForm(forms.Form):
    def __init__(self,questionnaire=None, *args, **kwargs):
        super(QuestionnaireForm, self).__init__(*args, **kwargs)
        for survey in questionnaire.survey_set.all() if questionnaire else []:
            self.fields[survey.id] = SurveyModelChoiceField( 
                queryset = PossibleAnswer.objects.filter(survey=survey), 
                widget = RadioSelect,
                empty_label = None,
                label =  survey.question 
                )

def questionnaire(request, id):
    questionnaire = Questionnaire.objects.get(id=id)
    surveys = questionnaire.survey_set.all()
    if request.method=="GET":
        initial = dict( (answer.survey.id, answer.id) 
                    for answer 
                    in request.user.possibleanswer_set.filter(survey__questionnaire = questionnaire)
                    )
        form = QuestionnaireForm(questionnaire, initial = initial)
        context = RequestContext( request, {
                "form": form,
                "title": questionnaire.name
                })
        return render(request, "surveys/present.html", context)
    else:
        form = QuestionnaireForm(data = request.POST)
        data = [(key,value) for key,value in form.data.iteritems() if key.isdigit()]
        for key,value in data:
            survey = Survey.objects.get(id = int(key))
            answers = request.user.possibleanswer_set.filter(survey=survey)
            request.user.possibleanswer_set.remove(*answers)
            answer = PossibleAnswer.objects.get(id=value)
            request.user.possibleanswer_set.add(answer)
        return render(request, "surveys/thanks.html")

    
