# from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import render  # For displaying in template
from django.views import generic  # For ListView and DetailView
from .models import Room, Reservation, Customer, Staff  # Import Models


def index(request):
    """
    This is the view for homepage.
    This is a function based view.
    """
    page_title = "Hotel Management System"  # For page title as well as heading
    total_num_rooms = Room.objects.all().count()
    available_num_rooms = Room.objects.exclude(reservation__isnull=False).count()
    total_num_reservations = Reservation.objects.all().count()
    total_num_staffs = Staff.objects.all().count()
    total_num_customers = Customer.objects.all().count()
    last_reserved_by = Reservation.objects.order_by('-reservation_date_time').all()[0]
    return render(
        request,
        'index.html',
        # context is whatever sent to the template.
        # the index of the dictionary i.e. title in 'title': page_title
        # is used as variable in templates
        # where as the next one is the variable of this function
        context={
            'title': page_title,
            'total_num_rooms': total_num_rooms,
            'available_num_rooms': available_num_rooms,
            'total_num_reservations': total_num_reservations,
            'total_num_staffs': total_num_staffs,
            'total_num_customers': total_num_customers,
            'last_reserved_by': last_reserved_by,
        }
    )


# For generic ListView or DetailView, the default templates should be stored in templates/{{app_name}}/{{template_name}}
# By default template_name = modelName_list || modelName_detail.
# eg room_list, room_detail
# @permission_required('main.can_view_staff')
class RoomListView(PermissionRequiredMixin, generic.ListView):
    """
    View for list of rooms.
    Implements generic ListView.
    """
    model = Room  # Chooses the model for listing objects
    paginate_by = 5  # By how many objects this has to be paginated
    title = "Room List"  # This is used for title and heading
    permission_required = 'main.can_view_room'

    # By default only objects of the model are sent as context
    # However extra context can be passed using field extra_context
    # Here title is passed.

    extra_context = {'title': title}

    # By default:
    # template_name = room_list
    # if you want to change it, use field template_name
    # here don't do this, since it is already done as default.
    # for own views, it can be done.

    def get_queryset(self):
        filter_value = self.request.GET.get('filter', 'all')
        if filter_value == 'all':
            filter_value = 0
        elif filter_value == 'avail':
            filter_value = 1
        try:
            new_context = Room.objects.filter(availability__in=[filter_value, 1])
        except ValidationError:
            raise Http404("Wrong filter argument given.")
        return new_context

    def get_context_data(self, **kwargs):
        context = super(RoomListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', 'all')
        return context


class RoomDetailView(PermissionRequiredMixin, generic.DetailView):
    """
    View for detail of room
    Implements generic DetailView
    """
    # The remaining are same as previous.
    model = Room
    title = "Room Information"
    permission_required = 'main.can_view_room'
    extra_context = {'title': title}


class ReservationListView(PermissionRequiredMixin, generic.ListView):
    """
        View for list of reservations.
        Implements generic ListView.
        """
    model = Reservation
    # queryset field selects the objects to be displayed by the query.
    # Here, the objects are displayed by reservation date time in descending order
    queryset = Reservation.objects.all().order_by('-reservation_date_time')
    title = "Reservation List"
    paginate_by = 3
    permission_required = 'main.can_view_reservation'
    extra_context = {'title': title}


class ReservationDetailView(PermissionRequiredMixin, generic.DetailView):
    """
    View for detail of reservation
    Implements generic DetailView
    """
    model = Reservation
    title = "Reservation Information"
    permission_required = 'main.can_view_reservation'
    raise_exception = True
    extra_context = {'title': title}


class CustomerDetailView(PermissionRequiredMixin, generic.DetailView):
    """
    View for detail of customer
    Implements generic DetailView
    """
    model = Customer
    title = "Customer Information"
    permission_required = 'main.can_view_customer'
    raise_exception = True
    extra_context = {'title': title}


class StaffDetailView(PermissionRequiredMixin, generic.DetailView):
    """
    View for detail of staff
    Implements generic DetailView
    """
    model = Staff
    title = "Staff Information"
    permission_required = 'main.can_view_staff_detail'
    extra_context = {'title': title}
