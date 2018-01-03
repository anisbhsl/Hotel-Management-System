from django.http import HttpResponse


# Create your views here.
# TODO Create views properly
def index(request):
    return HttpResponse('Successfully completed first app creation')
