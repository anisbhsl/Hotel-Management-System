from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.views import generic

from main.models import Facility
from .models import CheckIn


# Create your views here.

def payment_index(request):
    return HttpResponse("Payment")


class CheckInListView(PermissionRequiredMixin, generic.ListView):
    model = CheckIn
    paginate_by = 5
    permission_required = 'main.can_view_customer'


class CheckInDetailView(PermissionRequiredMixin, generic.DetailView):
    model = CheckIn
    permission_required = 'main.can_view_customer'
    num_facilities = Facility.objects.count()
    if not num_facilities:
        facilities = Facility.objects.none()
    else:
        facilities = Facility.objects.all()

    extra_context = {
        'facilities': facilities,
        'num_facilities': num_facilities,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checkin = context['checkin']
        new_rooms = checkin.rooms.split(', ')
        new_rooms = list(map(int, new_rooms))
        context['rooms'] = new_rooms
        return context
