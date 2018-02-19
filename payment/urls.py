from django.urls import path

from . import views

urlpatterns = [
    path('', views.payment_index, name='payment-index'),
    path('check_ins/', views.CheckInListView.as_view(), name='check_in-list'),
    path('check_in/<str:pk>', views.CheckInDetailView.as_view(), name='check_in-detail'),
]
