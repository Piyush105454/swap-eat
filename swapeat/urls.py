from django.contrib import admin
from django.urls import path, include
from swapfood import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home2/explore/', views.explore, name='explore'),
    path('home2/postmeal/', views.postmeal, name='postmeal'),
    path('home2/chat/', views.chat, name='chat'),
    path('home2/post/', views.post, name='post'),
    path("chat-api/", views.chat_api, name="chat_api"),
    
    path('home2/Home/', views.Home, name='Home'),
    path('admin/', admin.site.urls),
    path('chat/', include('swapfood.urls')), 
      # Fixed missing parenthesis

    path('signup/', views.SignupPage, name='signup'),  # Renamed for clarity
    path('home2/', views.HomePage2, name='home2'),
    path('login/', views.LoginPage, name='login'),
    path('', views.HomePage, name='home'),  # Fixed trailing slash consistency
    path('home/logout/', views.LogoutPage, name='logout'),
    # Changed to use a different view for clarity
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
