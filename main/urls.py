from django.urls import path
from django.views import generic

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/', views.RoomListView.as_view(), name='rooms'),
]
