from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/', views.RoomListView.as_view(), name='rooms'),  # List of Rooms
    path('reservations/', views.ReservationListView.as_view(), name='reservations'),  # List of Reservations
    path('room/<int:pk>', views.RoomDetailView.as_view(), name='room-detail'),  # Detail of each room
    # Detail of each reservation
    path('reservation/<str:pk>', views.ReservationDetailView.as_view(), name='reservation-detail'),
    path('customer/<str:pk>', views.CustomerDetailView.as_view(), name='customer-detail'),  # Detail of each customer
    path('staff/<str:pk>', views.StaffDetailView.as_view(), name='staff-detail'),  # Detail of staff

]
