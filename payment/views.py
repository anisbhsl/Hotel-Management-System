from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views import generic

from main.models import Facility, Reservation
from .forms import CheckoutRequestForm
from .models import CheckIn, CheckOut


# Create your views here.
@permission_required('main.can_view_staff', login_url='login')
def payment_index(request):
    title = "Payment Dashboard"
    num_of_reservations = Reservation.objects.all().count()
    num_of_check_ins = CheckIn.objects.all().count()
    last_checked_in = CheckIn.objects.none()
    if num_of_check_ins > 0:
        last_checked_in = CheckIn.objects.get_queryset().latest('check_in_date_time')
    return render(
        request,
        'payment_index.html', {
            'title': title,
            'num_of_reservations': num_of_reservations,
            'num_of_check_ins': num_of_check_ins,
            'last_checked_in': last_checked_in,
        }
    )


class CheckInListView(PermissionRequiredMixin, generic.ListView, generic.FormView):
    model = CheckIn
    paginate_by = 5
    permission_required = 'main.can_view_customer'
    title = "Check-In List"
    form_class = CheckoutRequestForm
    extra_context = {
        'title': title,
    }


class CheckInDetailView(PermissionRequiredMixin, generic.DetailView):
    model = CheckIn
    permission_required = 'main.can_view_customer'
    num_facilities = Facility.objects.count()
    title = "Check-In Detail"
    if not num_facilities:
        facilities = Facility.objects.none()
    else:
        facilities = Facility.objects.all()

    extra_context = {
        'facilities': facilities,
        'num_facilities': num_facilities,
        'title': title,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checkin = context['checkin']
        rooms = checkin.rooms
        if rooms:
            new_rooms = checkin.rooms.split(', ')
            new_rooms = list(map(int, new_rooms))
            context['rooms'] = new_rooms
        return context


class CheckOutListView(PermissionRequiredMixin, generic.ListView):
    model = CheckOut
    paginate_by = 5
    permission_required = 'main.can_view_customer'
    title = "Check-Out List"
    extra_context = {
        'title': title,
    }


class CheckOutDetailView(PermissionRequiredMixin, generic.DetailView):
    model = CheckOut
    permission_required = 'main.can_view_customer'
    title = "Check-Out Detail"
    extra_context = {
        'title': title,
    }


def checkout_confirm(request):
    return render(
        request,
        'confirm_checkout.html', {
            'title': 'Confirm Checkout'
        }
    )
