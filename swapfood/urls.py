from django.urls import path
from . import views

urlpatterns = [
    path('create-room/', views.CreateRoom, name='create-room'),  # Corrected path
    path('<str:room_name>/<str:username>/', views.MessageView, name='room'),
]
