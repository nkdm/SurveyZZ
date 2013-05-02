from django.contrib import admin
from surveys.models import Survey,PossibleAnswer,Vote

admin.site.register(Survey)
admin.site.register(PossibleAnswer)
admin.site.register(Vote)
