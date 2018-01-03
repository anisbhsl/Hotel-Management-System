from django.http import HttpResponse
from django.shortcuts import render



# Create your views here.
# TODO Create views properly
def index(request):
    return render(request,'main/base.html')
