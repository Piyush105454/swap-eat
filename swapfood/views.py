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
from .forms import InvitationForm, SearchForm
from django.core.exceptions import ValidationError
import random
import requests
import json

def post_food(request):
    if request.method == "POST":
        form = FoodPostForm(request.POST, request.FILES)
        if form.is_valid():
            food_post = form.save(commit=False)
            food_post.latitude = request.POST.get("latitude")
            food_post.longitude = request.POST.get("longitude")
            food_post.save()
            return redirect("map")  # Redirect to map page
    else:
        form = FoodPostForm()
    
    return render(request, "post_food.html", {"form": form})

def map_view(request):
    food_posts = list(FoodPost.objects.values("latitude", "longitude", "photo", "name", "radius", "created_at", "id"))

    # Convert datetime objects to string
    for post in food_posts:
        post["created_at"] = post["created_at"].isoformat()

    return render(request, "map.html", {"food_posts": json.dumps(food_posts)})
    
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
@login_required
def postmeal(request):
    if request.method == "POST":
        name = request.POST.get("taste")
        description = request.POST.get("tags")
        radius = request.POST.get("radius")
        image = request.FILES.get("image")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        # Convert latitude and longitude to float, as they are coming from the form
        try:
            latitude = float(latitude) if latitude else None
        except ValueError:
            latitude = None

        try:
            longitude = float(longitude) if longitude else None
        except ValueError:
            longitude = None

        # Create a new Meal object with the user's location
        Meal.objects.create(
            name=name,
            description=description,
            radius=radius,
            image=image,
            latitude=latitude,
            longitude=longitude
        )

        return redirect('map')

    return render(request, "postmeal.html")

    
@login_required
def invite_member(request):
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.user = request.user
            invitation.save()
            
            # Send invitation email
            send_mail(
                'You are invited to join our website!',
                'Please join us at our website: [URL]',
                'swapeatmail@gmail.com',  # From email
                [invitation.email],   # To email
                fail_silently=False,
            )
            return redirect('home')  # Redirect to a success page or home
    else:
        form = InvitationForm()

    return render(request, 'invite_member.html', {'form': form})

# Search meals view
def search_meals(request):
    meals = None
    query = ''
    if 'q' in request.GET:
        query = request.GET['q']
        meals = Meal.objects.filter(name__icontains=query)
    
    return render(request, 'search_meals.html', {'meals': meals, 'query': query})
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
@login_required
def chat(request):
    """ Opens the chat page where the user can enter a username and search for a chat. """
    return render(request, 'message.html')

@login_required
def MessageView(request, room_name=None, username=None):
    """ Handles chat messages, fetching the correct room and messages. """
    
    # Ensure room_name and username are provided
    if not room_name or not username:
        return redirect('chat')  # Redirect to chat search if missing
    
    get_room, created = Room.objects.get_or_create(room_name=room_name)

    if request.method == 'POST':
        message = request.POST['message']
        new_message = Message(room=get_room, sender=request.user, message=message)
        new_message.save()

    get_messages = Message.objects.filter(room=get_room)

    context = {
        "messages": get_messages,
        "chat_user": username,
        "room_name": room_name,
    }
    return render(request, 'message.html', context)


@login_required
def search_users(request):
    """ Searches users by username """
    query = request.GET.get("q", "").strip()
    users = User.objects.filter(username__icontains=query).exclude(username=request.user.username)[:5]
    return JsonResponse({"users": [{"username": u.username} for u in users]})

@login_required
def get_chat_messages(request):
    room_name = request.GET.get("room_name")
    try:
        room = Room.objects.get(room_name=room_name)
        messages = Message.objects.filter(room=room).order_by("id")
        return JsonResponse({
            "messages": [{"sender": msg.sender.username, "message": msg.message} for msg in messages]
        })
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room does not exist"}, status=404)
