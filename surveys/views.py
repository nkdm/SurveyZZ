# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from surveys.models import Survey, PossibleAnswer, User, Questionnaire, submitAnswer
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
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple

class SurveyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self,obj):
        return obj.text

class SurveyModelMultipleChoiceField(forms.ModelChoiceField):
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
        answer = PossibleAnswer.objects.get(id=optionId)
        survey = answer.survey
        answers = request.user.possibleanswer_set.filter(survey=survey)
        request.user.possibleanswer_set.remove(*answers)
        request.user.possibleanswer_set.add(answer)

        context = RequestContext(request,{
                'answer':answer.text
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
            if survey.type == 'm':
                self.fields[survey.id] = SurveyModelMultipleChoiceField( 
                    queryset = PossibleAnswer.objects.filter(survey=survey), 
                    label =  survey.question,
                    widget = CheckboxSelectMultiple,
                    empty_label = None
                    )
            else:
                self.fields[survey.id] = SurveyModelChoiceField( 
                    queryset = PossibleAnswer.objects.filter(survey=survey),
                    widget = RadioSelect,
                    empty_label = None,
                    label =  survey.question 
                    )


def unList(x):
    if isinstance(x,list):
        if len(x) == 1:
            return x[0]
    return x

import collections
def questionnaire(request, id):
    questionnaire = Questionnaire.objects.get(id=id)
    surveys = questionnaire.survey_set.all()
    if request.method=="GET":
        initialLists = collections.defaultdict(list)
        for answer in request.user.possibleanswer_set.filter(survey__questionnaire = questionnaire):
            initialLists[answer.survey.id].append(answer.id)
        
        initial = { key:unList(item) for key,item in initialLists.iteritems()  }
            
        form = QuestionnaireForm(questionnaire, initial = initial)
        context = RequestContext( request, {
                "form": form,
                "title": questionnaire.name
                })
        return render(request, "surveys/present.html", context)
    else:
        postDict = dict(request.POST)
        data = [(key,value) for key,value in postDict.iteritems() if key.isdigit()]
        choicesTexts = []
        for key,value in data:
            answer = PossibleAnswer.objects.filter(id__in=value)
            submitAnswer(request.user,answer)
        context = Context({ "answer": ", ".join(choicesTexts)})
        return render(request, "surveys/thanks.html", context)

