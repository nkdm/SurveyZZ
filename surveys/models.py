from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Survey(models.Model):
    question = models.CharField(max_length=150)
    def __unicode__(self):
        return self.question

class PossibleAnswer(models.Model):
    survey = models.ForeignKey(Survey)
    text = models.CharField(max_length=150)
    voters = models.ManyToManyField(User, blank = True)
    def __unicode__(self):
        return self.survey.question + " : " + self.text



