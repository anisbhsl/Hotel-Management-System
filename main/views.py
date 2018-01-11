from django.shortcuts import render


# Create your views here.
# TODO Create views properly
def index(request):
    message = "It is working."
    page_title = "Hotel Management System"
    return render(
        request,
        'main/index.html',
        context={
            'message': message,
            'title': page_title,
        }
    )
