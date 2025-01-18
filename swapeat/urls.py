from django.contrib import admin
from django.urls import path, include
from swapfood import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home2/explore/', views.explore, name='explore'),
    path('home2/postmeal/', views.postmeal, name='postmeal'),
    path('admin/', admin.site.urls),
    path('', include('swapfood.urls')),  # Fixed missing parenthesis

    path('signup/', views.SignupPage, name='signup'),  # Renamed for clarity
    path('home2/', views.HomePage2, name='home2'),
    path('login/', views.LoginPage, name='login'),
    path('home/', views.HomePage, name='home/'),  # Fixed trailing slash consistency
    path('logout/', views.LogoutPage, name='logout'),
    path('home2/upload/', views.upload, name='upload'),  # Changed to use a different view for clarity
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
