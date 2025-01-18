"""
URL configuration for swapeat project.

The `urlpatterns` list routes URLs to views. For more information, please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from swapfood import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home2/explore/', views.explore, name='explore'),
    path('home2/postmeal/', views.postmeal, name='postmeal'),
    path('admin/', admin.site.urls),
    path('', include('ChatApp.urls'))

   
    path('S', views.SignupPage, name='signup'),
    path('home2/', views.HomePage2, name='home2'),
    path('login/', views.LoginPage, name='login'),
    path('home/', views.HomePage, name='home'),  # Add a trailing slash for consistency
    path('logout/', views.LogoutPage, name='logout'),
    path('home2/upload/', views.HomePage2, name='upload'),  # Add a trailing slash
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
