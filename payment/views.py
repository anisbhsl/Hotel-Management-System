from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction, IntegrityError
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from main.models import Facility, Reservation, Staff
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
    queryset = CheckIn.objects.all().order_by('-check_in_date_time')
    allow_empty = True
    permission_required = 'main.can_view_customer'
    title = "Check-In List"
    form_class = CheckoutRequestForm
    extra_context = {
        'title': title,
    }
    success_url = reverse_lazy('check_out-list')

    @transaction.atomic
    def form_valid(self, form):
        try:
            with transaction.atomic():
                checkout = form.save(commit=False)
                checkout.user = self.request.user
                checkout.save()
                for room in checkout.check_in.reservation.room_set.all():
                    room.reservation = None
                    room.save()
        except IntegrityError:
            raise Http404
        return super().form_valid(form)


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
        staff = Staff.objects.filter(user=checkin.user)
        if not staff.count():
            staff = Staff.objects.none()
        else:
            staff = Staff.objects.get(user=checkin.user)
        context['staff'] = staff
        if rooms:
            new_rooms = checkin.rooms.split(', ')
            new_rooms = list(map(int, new_rooms))
            context['rooms'] = new_rooms
        return context


class CheckOutListView(PermissionRequiredMixin, generic.ListView):
    model = CheckOut
    paginate_by = 5
    allow_empty = True
    queryset = CheckOut.objects.all().order_by('-check_out_date_time')
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checkout = context['checkout']

        staff = Staff.objects.filter(user=checkout.user)
        if not staff.count():
            staff = Staff.objects.none()
        else:
            staff = Staff.objects.get(user=checkout.user)
        context['staff'] = staff

        return context

