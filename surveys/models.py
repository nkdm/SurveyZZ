from django.db import models
from django.contrib.auth.models import User
import re

# Create your models here.
class Survey(models.Model):
    question = models.CharField(max_length=150)
    def __unicode__(self):
        return self.question

class PossibleAnswer(models.Model):
    survey = models.ForeignKey(Survey)
    text = models.CharField(max_length=150)
    def __unicode__(self):
        return self.survey.question + " : " + self.text

class Vote(models.Model):
    choice = models.ForeignKey(PossibleAnswer)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.choice.survey.question + " : " + self.user.username  + " : " + self.choice.text
