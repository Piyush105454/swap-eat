from django.contrib import admin
from django.urls import path, include
from swapfood import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('post/explore/', views.explore, name='explore'),
    path('post/postmeal/', views.postmeal, name='postmeal'),
    path('post/chat/', views.chat, name='chat'),
    path('post/', views.post, name='post'),
    path("chat-api/", views.chat_api, name="chat_api"),
    path('verify-otp/<int:user_id>/', views.VerifyOTP, name='verify_otp'),
    path('post/notification/', views.notification, name='notification'),
    path('admin/', admin.site.urls),
    path('chat/', include('swapfood.urls')), 
      # Fixed missing parenthesis
    path('map/', views.map_view, name='map'),  
    path('post_food/', views.post_food, name='post_food'),  
    path('signup/', views.SignupPage, name='signup'),  # Renamed for clarity
    path('post/home2/', views.HomePage2, name='home2'),
    path('login/', views.LoginPage, name='login'),
    path('', views.HomePage, name='home'),  # Fixed trailing slash consistency
    path('home/logout/', views.LogoutPage, name='logout'),
    # Changed to use a different view for clarity
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
