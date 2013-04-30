from django.db import models
import re

# Create your models here.
class Survey(models.Model):
    question = models.CharField(max_length=150)

class Vote(models.Model):
    survey = models.ForeignKey(Survey)
    choice_text = models.CharField(max_length=50)
