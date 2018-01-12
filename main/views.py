from django.shortcuts import render
from django.views import generic

from .models import Room


# Create your views here.
# TODO Create views properly
def index(request):
    message = "It is working."
    page_title = "Hotel Management System"
    return render(
        request,
        'index.html',
        context={
            'message': message,
            'title': page_title,
        }
    )


class RoomListView(generic.ListView):
    model = Room
    paginate_by = 5
