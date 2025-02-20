from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import Room, Message, Meal, UserOTP
from .models import FoodPost
from .forms import FoodPostForm
import random
import requests
import json

def post_food(request):
    if request.method == "POST":
        form = FoodPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("map")  # Redirect to map page
    else:
        form = FoodPostForm()
    return render(request, "post_food.html", {"form": form})

def map_view(request):
    food_posts = list(Meal.objects.values("latitude", "longitude", "image"))  # Convert QuerySet to list
    return render(request, "map.html", {"food_posts": food_posts})
# Helper function: Generate OTP
def generate_otp():
    return random.randint(100000, 999999)

# Helper function: Send OTP email
def send_otp_email(email, otp):
    subject = "Your OTP for Email Verification"
    message = f"Hello,\n\nYour OTP for registration is {otp}.\n\nThank you!"
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])

# Signup with OTP
def SignupPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        uname = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if User.objects.filter(username=uname).exists():
            return HttpResponse("Username already exists! Please choose a different one.")
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already registered!")
        if pass1 != pass2:
            return HttpResponse("Your password and confirm password do not match!")

        # Create inactive user
        my_user = User.objects.create_user(username=uname, email=email, password=pass1, first_name=name, is_active=False)
        my_user.save()

        # Generate OTP and save it
        otp = generate_otp()
        UserOTP.objects.create(user=my_user, otp=otp)

        # Send OTP to user's email
        send_otp_email(email, otp)

        # Redirect to OTP verification page
        return redirect('verify_otp', user_id=my_user.id)
    return render(request, 'signup.html')

# OTP Verification View
def VerifyOTP(request, user_id):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            user_otp = UserOTP.objects.get(user_id=user_id, otp=otp)
            user = user_otp.user
            user.is_active = True  # Activate user account
            user.save()
            user_otp.delete()  # Remove OTP after verification
            return redirect('login')
        except UserOTP.DoesNotExist:
            return HttpResponse("Invalid OTP!")
    return render(request, 'verify_otp.html', {'user_id': user_id})

# Login View
def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

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

# Logout View
def LogoutPage(request):
    logout(request)
    return redirect('login')

# Home Page View

def HomePage(request):
    return render(request, 'home.html')

# Upload Image and Display
@login_required
def HomePage2(request):
    if request.method == 'POST' and request.FILES.get('image'):
        pic = request.FILES['image']
        file_path = default_storage.save(f'uploads/{pic.name}', pic)
        file_url = settings.MEDIA_URL + file_path
        file_name = pic.name
        return render(request, 'home2.html', {'file_url': file_url, 'file_name': file_name})
    return render(request, 'home2.html')

# Explore Section
@login_required
def explore(request):
    return render(request, 'explore.html')

# Chat Section
@login_required
def chat(request):
    return render(request, 'index.html')

# Post Meals Section
@login_required
def post(request):
    meals = Meal.objects.all()
    return render(request, "profile.html", {"meals": meals})

# Add a New Meal Post
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

# Meal Display Home
@login_required
def notification(request):
    meals = Meal.objects.all()
    return render(request, "notification.html", {"meals": meals})

# Chatbot API (Gemini Integration)
def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_question = data.get("question", "")

        # Gemini API URL
        gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

        payload = {
            "contents": [{"parts": [{"text": user_question}]}]
        }

        headers = {
            "Authorization": f"Bearer {settings.GEMINI_API_KEY}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(gemini_url, json=payload, headers=headers)
            if response.status_code == 200:
                gemini_response = response.json()
                answer = gemini_response.get("content", "Sorry, I couldn't generate a response.")
            else:
                answer = f"Error: Unable to connect to Gemini API. Status code: {response.status_code}"
        except Exception as e:
            answer = f"An error occurred: {str(e)}"

        return JsonResponse({"answer": answer})

    return JsonResponse({"error": "Invalid request method."}, status=400)

# Create a Room for Chat
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

# Message Handling in Chat Room
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
