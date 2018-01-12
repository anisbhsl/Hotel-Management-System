from django.shortcuts import render
from django.views import generic

from .models import Room, Reservation, Customer, Staff


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
    title = "Room List"
    extra_context = {'title': title}


class RoomDetailView(generic.DetailView):
    model = Room


class ReservationListView(generic.ListView):
    model = Reservation
    queryset = Reservation.objects.all().order_by('-reservation_date_time')
    title = "Reservation List"
    paginate_by = 10
    extra_context = {'title': title}


class ReservationDetailView(generic.DetailView):
    model = Reservation


class CustomerDetailView(generic.DetailView):
    model = Customer


class StaffDetailView(generic.DetailView):
    model = Staff
