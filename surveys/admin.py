from django.contrib import admin
from surveys.models import Survey,PossibleAnswer

from django.contrib import admin
class PossibleAnswerAdmin(admin.ModelAdmin):
    exclude = ['voters']

admin.site.register(Survey)
admin.site.register(PossibleAnswer,PossibleAnswerAdmin)
