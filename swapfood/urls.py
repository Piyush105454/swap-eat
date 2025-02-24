from django.urls import path
from . import views

urlpatterns = [
    path("search_users/", views.search_users, name="search_users"),
    path("chat/<int:receiver_id>/", views.chat_view, name="chat_view"),
]
