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
class RoomListView(generic.ListView):
    """
    View for list of rooms.
    Implements generic ListView.
    """
    model = Room  # Chooses the model for listing objects
    paginate_by = 5  # By how many objects this has to be paginated
    title = "Room List"  # This is used for title and heading
    # By default only objects of the model are sent as context
    # However extra context can be passed using field extra_context
    # Here title is passed.
    extra_context = {'title': title}
    # By default:
    # template_name = room_list
    # if you want to change it, use field template_name
    # here don't do this, since it is already done as default.
    # for own views, it can be done.


class RoomDetailView(generic.DetailView):
    """
    View for detail of room
    Implements generic DetailView
    """
    # The remaining are same as previous.
    model = Room
    title = "Room Information"
    extra_context = {'title': title}


class ReservationListView(generic.ListView):
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
    extra_context = {'title': title}


class ReservationDetailView(generic.DetailView):
    """
    View for detail of reservation
    Implements generic DetailView
    """
    model = Reservation
    title = "Reservation Information"
    extra_context = {'title': title}


class CustomerDetailView(generic.DetailView):
    """
    View for detail of customer
    Implements generic DetailView
    """
    model = Customer
    title = "Customer Information"
    extra_context = {'title': title}


class StaffDetailView(generic.DetailView):
    """
    View for detail of staff
    Implements generic DetailView
    """
    model = Staff
    title = "Staff Information"
    extra_context = {'title': title}
