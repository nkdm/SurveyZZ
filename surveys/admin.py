from django.contrib import admin
from surveys.models import Survey, PossibleAnswer, Questionnaire

from django.contrib import admin
class PossibleAnswerAdmin(admin.ModelAdmin):
    exclude = ['voters']

admin.site.register(Survey)
admin.site.register(Questionnaire)
admin.site.register(PossibleAnswer,PossibleAnswerAdmin)
