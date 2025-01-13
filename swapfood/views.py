from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
# Create your views here.
from django.conf import settings
from .models import user
# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render (request,'home.html')
def HomePage2(request):
    if request.method == 'POST' and request.FILES.get('image'):
        pic = request.FILES['image']
        file_path = default_storage.save(f'uploads/{pic.name}', pic)
        # Do something with the file path (e.g., link it to a different model)
        file_url = settings.MEDIA_URL + file_path
        # Extract the file name from the uploaded file
        file_name = pic.name
        
        # Pass both the file URL and file name to the template
        return render(request, 'home2.html', {'file_url': file_url, 'file_name': file_name})
       
    return render(request, 'home2.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')
