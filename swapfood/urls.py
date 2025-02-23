from . import views
from django.urls import path

urlpatterns = [
    path('', views.MessageView, name='MessageView'),
    path('<str:room_name>/<str:username>/', views.MessageView, name='room'),
]
