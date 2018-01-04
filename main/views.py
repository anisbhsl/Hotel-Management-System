from django.shortcuts import render


# Create your views here.
# TODO Create views properly
def index(request):
    hello = "Hello"
    return render(request, 'main/index.html', context={'hello_name':hello})
