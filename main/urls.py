from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    # The field option name, should be unique as it is a unique identifier.
    # e.g. if you want to use the hyperlink of index page, don't use hardcoded url like
    # href="/main/" as if it is changed we have to change all the occurrences of it.
    # to solve this, use the value from name field. for above example use
    # href="{% url 'index' %}
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('rooms/', views.RoomListView.as_view(), name='rooms'),  # List of Rooms
    path('reservations/', views.ReservationListView.as_view(), name='reservations'),  # List of Reservations
    # <int:pk> takes the argument sent in urls.
    path('room/<int:pk>', views.RoomDetailView.as_view(), name='room-detail'),  # Detail of each room
    # Detail of each reservation
    path('reservation/<str:pk>', views.ReservationDetailView.as_view(), name='reservation-detail'),
    path('customer/<str:pk>', views.CustomerDetailView.as_view(), name='customer-detail'),  # Detail of each customer
    path('staff/<str:pk>', views.StaffDetailView.as_view(), name='staff-detail'),  # Detail of staff
    path('profile/', login_required(views.ProfileView.as_view()), name='profile'),
    path('guests/', views.GuestListView.as_view(), name='guest-list'),
    path('reserve/', views.reserve, name='reserve'),  # For reservation
]
