from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.conf import settings
from .models import Room, Message, Meal

# Public Views
def SignupPage(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home if already logged in

    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if User.objects.filter(username=uname).exists():
            return HttpResponse("Username already exists! Please choose a different one.")
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already registered!")
        if pass1 != pass2:
            return HttpResponse("Your password and confirm password do not match!")
        
        # Create the user
        my_user = User.objects.create_user(username=uname, email=email, password=pass1)
        my_user.save()
        return redirect('login')
    return render(request, 'signup.html')

def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!")
    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

# Protected Views
@login_required
def HomePage(request):
    return render(request, 'home.html')

@login_required
def HomePage2(request):
    if request.method == 'POST' and request.FILES.get('image'):
        pic = request.FILES['image']
        file_path = default_storage.save(f'uploads/{pic.name}', pic)
        file_url = settings.MEDIA_URL + file_path
        file_name = pic.name
        return render(request, 'home2.html', {'file_url': file_url, 'file_name': file_name})
    return render(request, 'home2.html')

@login_required
def explore(request):
    return render(request, 'explore.html')

@login_required
def chat(request):
    return render(request, 'index.html')

@login_required
def postmeal(request):
    if request.method == "POST":
        name = request.POST.get("taste")
        description = request.POST.get("tags")
        radius = request.POST.get("radius")
        image = request.FILES.get("image")
        Meal.objects.create(name=name, description=description, radius=radius, image=image)
        return redirect('Home')  # Ensure this line is correctly indented
    return render(request, "postmeal.html")

@login_required
def Home(request):
    meals = Meal.objects.all()
    return render(request, "Home.html", {"meals": meals})

# Chat Room Functionality
@login_required
def CreateRoom(request):
    if request.method == 'POST':
        username = request.POST['username']
        room = request.POST['room']

        try:
            get_room = Room.objects.get(room_name=room)
            return redirect('room', room_name=room, username=username)

        except Room.DoesNotExist:
            new_room = Room(room_name=room)
            new_room.save()
            return redirect('room', room_name=room, username=username)

    return render(request, 'index.html')

@login_required
def MessageView(request, room_name, username):
    get_room = Room.objects.get(room_name=room_name)

    if request.method == 'POST':
        message = request.POST['message']
        new_message = Message(room=get_room, sender=username, message=message)
        new_message.save()

    get_messages = Message.objects.filter(room=get_room)

    context = {
        "messages": get_messages,
        "user": username,
        "room_name": room_name,
    }
    return render(request, 'message.html', context)
