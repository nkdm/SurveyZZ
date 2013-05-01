# Create your views here.
from django.http import HttpResponse
from surveys.models import Survey
from django.template import loader, Context

def index(request):
    allSurveys = Survey.objects.all()
    context = Context({
        "surveys": allSurveys,
    })
    template = loader.get_template("surveys/index.html")
    return HttpResponse(template.render(context))
