from django.db import models
import re

# Create your models here.
class Survey(models.Model):
    question = models.CharField(max_length=150)
    def __unicode__(self):
        return self.question

class Vote(models.Model):
    survey = models.ForeignKey(Survey)
    choice_text = models.CharField(max_length=50)

class PossibleAnswer(models.Model):
    survey = models.ForeignKey(Survey)
    text = models.CharField(max_length=150)
    def __unicode__(self):
        return self.text

