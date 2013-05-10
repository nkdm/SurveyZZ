from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Questionnaire(models.Model):
    name = models.CharField(max_length=150)
    def __unicode__(self):
        return self.name

SurveyType = (
    ('m', "Multiple choice"),
    ('s', "Single choice"),
 )

class Survey(models.Model):
    question = models.CharField(max_length=150)
    questionnaire = models.ForeignKey(Questionnaire)
    type = models.CharField(max_length=1, choices=SurveyType)
    def __unicode__(self):
        return self.question

class PossibleAnswer(models.Model):
    survey = models.ForeignKey(Survey)
    text = models.CharField(max_length=150)
    voters = models.ManyToManyField(User, blank = True)
    def __unicode__(self):
        return self.survey.question + " : " + self.text

def submitAnswer(user,answer):
    survey = answer[0].survey
    answers = user.possibleanswer_set.filter(survey=survey)
    user.possibleanswer_set.remove(*answers)
    user.possibleanswer_set.add(*answer)
