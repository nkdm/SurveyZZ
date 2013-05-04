from surveys.models import Survey, PossibleAnswer
from django.contrib.auth.models import User
from random import randrange

usernames = ["user{0}".format(i) for i in range(0,50)]
def CreateUsers():
    for username in usernames:
        user = User.objects.create_user(username,username+"@"+username,"user")
        user.save()


def Vote():
    surveys = Survey.objects.all()
    users = User.objects.all()
    for survey in surveys:
        answers = PossibleAnswer.objects.filter(survey = survey)
        for user in users:
            print user,survey
            answers[randrange(answers.count())].voters.add(user)
            
