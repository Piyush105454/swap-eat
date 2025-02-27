from django.contrib import admin
from django.urls import path, include
from swapfood import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("chat/", views.chat, name="chat"),  # Fixed duplicate include issue
    path("chat-api/", views.chat_api, name="chat_api"),
    path('my-form/',views.my_view, name='my_form'), 
    path("post/explore/", views.explore, name="explore"),
    path("post/", views.post, name="post"),
    path("verify-otp/<int:user_id>/", views.VerifyOTP, name="verify_otp"),
    path("invite/", views.invite_member, name="invite_member"),
    path("search/", views.search_meals, name="search_meals"),
    path("post/notification/", views.notification, name="notification"),
    path("map/", views.map_view, name="map"),
    path("post_food/", views.post_food, name="post_food"),
    path("signup/", views.SignupPage, name="signup"),
    path("login/", views.LoginPage, name="login"),
    path("logout/", views.LogoutPage, name="logout"),
    path("", views.HomePage, name="home"),  # Ensure homepage is correctly defined
    path("admin/", admin.site.urls),  # Keep this at the bottom
    path('chat/', include('swapfood.urls')), 
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
