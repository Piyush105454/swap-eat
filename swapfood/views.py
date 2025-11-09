from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import ValidationError

from .models import Room, Message, UserOTP, FoodPost, FoodImage
from .forms import FoodPostForm, InvitationForm, SearchForm, FoodImageForm
from .serializers import FoodImageSerializer
from .spoonacular_api import analyze_food_image  

from geopy.distance import geodesic
import networkx as nx
import osmnx as ox
import random
import requests
import json
import base64


# ============================================================
# IMAGE UPLOAD + SPOONACULAR ANALYSIS
# ============================================================

def upload_food_image(request):
    form = FoodImageForm()
    image_url = None
    analysis_result = None

    if request.method == 'POST':
        form = FoodImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            image_url = uploaded_image.image.url
            image_path = uploaded_image.image.path

            analysis_result = analyze_food_image(image_path)

    return render(request, 'upload.html', {
        'form': form,
        'image_url': image_url,
        'analysis_result': analysis_result
    })


# ============================================================
# FIND NEAREST FOOD POST
# ============================================================

def find_nearest_post(user_lat, user_lon):
    min_distance = float("inf")
    nearest_post = None

    for post in FoodPost.objects.all():
        distance = geodesic((user_lat, user_lon), (post.latitude, post.longitude)).km
        if distance < min_distance:
            min_distance = distance
            nearest_post = post

    return nearest_post


# ============================================================
# SHORTEST PATH USING OSM
# ============================================================

def get_shortest_path(request):
    try:
        user_lat = float(request.GET.get("lat"))
        user_lon = float(request.GET.get("lon"))

        nearest_post = find_nearest_post(user_lat, user_lon)
        if not nearest_post:
            return JsonResponse({"error": "No nearby posts found"}, status=400)

        G = ox.graph_from_place("India", network_type="walk")

        orig_node = ox.distance.nearest_nodes(G, X=user_lon, Y=user_lat)
        dest_node = ox.distance.nearest_nodes(G, X=nearest_post.longitude, Y=nearest_post.latitude)

        shortest_route = nx.shortest_path(G, orig_node, dest_node, weight="length")

        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_route]

        return JsonResponse({
            "route": route_coords,
            "food_post": {
                "name": nearest_post.name,
                "latitude": nearest_post.latitude,
                "longitude": nearest_post.longitude,
                "location": nearest_post.location,
            }
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ============================================================
# POST FOOD
# ============================================================

@login_required
def post_food(request):
    if request.method == "POST":
        form = FoodPostForm(request.POST, request.FILES)
        if form.is_valid():
            food_post = form.save(commit=False)
            food_post.user = request.user
            food_post.latitude = request.POST.get("latitude")
            food_post.longitude = request.POST.get("longitude")
            food_post.save()

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": True})

            return redirect("post_food")

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": form.errors})

    food_posts = list(FoodPost.objects.values(
        "latitude", "longitude", "photo", "name", "radius", "location", "created_at", "id"
    ))

    for post in food_posts:
        post["created_at"] = post["created_at"].isoformat()

    return render(request, "post_food.html", {
        "form": FoodPostForm(),
        "food_posts": json.dumps(food_posts)
    })


# ============================================================
# SIMPLE VIEW
# ============================================================

def my_view(request):
    form = FoodPostForm()
    submitted_data = None

    if request.method == "POST":
        form = FoodPostForm(request.POST)
        if form.is_valid():
            submitted_data = form.cleaned_data
            form = FoodPostForm()

    return render(request, 'my_template.html', {'form': form, 'submitted_data': submitted_data})


def map_view(request):
    food_posts = list(FoodPost.objects.values("latitude", "longitude", "photo", "name", "radius", "created_at", "id"))

    for post in food_posts:
        post["created_at"] = post["created_at"].isoformat()

    return render(request, "map.html", {"food_posts": json.dumps(food_posts)})


# ============================================================
# OTP SYSTEM
# ============================================================

def generate_otp():
    return random.randint(100000, 999999)


def send_otp_email(email, otp):
    subject = "Your OTP for Email Verification"
    message = f"Hello,\n\nYour OTP for registration is {otp}.\n\nThank you!"
    from_email = settings.EMAIL_HOST_USER

    try:
        send_mail(subject, message, from_email, [email], fail_silently=False)
        return True
    except Exception:
        return False


# ============================================================
# SIGNUP (AUTO LOGIN IF EMAIL FAILS)
# ============================================================

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
            return HttpResponse("Username already exists!")
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already registered!")
        if pass1 != pass2:
            return HttpResponse("Passwords do not match!")

        user = User.objects.create_user(
            username=uname, email=email, password=pass1, first_name=name, is_active=False
        )

        otp = generate_otp()
        UserOTP.objects.create(user=user, otp=str(otp))

        email_sent = send_otp_email(email, otp)

        if email_sent:
            return redirect('verify_otp', user_id=user.id)
        else:
            # auto activate & go to login
            user.is_active = True
            user.save()
            return redirect('login')

    return render(request, 'signup.html')


# ============================================================
# VERIFY OTP
# ============================================================

def VerifyOTP(request, user_id):
    if request.method == 'POST':
        otp = request.POST.get('otp')

        try:
            user_otp = UserOTP.objects.get(user_id=user_id, otp=otp)
            user = user_otp.user
            user.is_active = True
            user.save()
            user_otp.delete()
            return redirect('login')
        except UserOTP.DoesNotExist:
            return HttpResponse("Invalid OTP!")

    return render(request, 'verify_otp.html', {'user_id': user_id})


# ============================================================
# LOGIN / LOGOUT / HOME
# ============================================================

def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user:
            login(request, user)
            return redirect('home')
        return HttpResponse("Username or Password is incorrect!")

    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')


def HomePage(request):
    return render(request, 'home.html')


def pf(request):
    return render(request, 'pf.html')


# ============================================================
# FOOD EXPLORE / POSTS
# ============================================================

@login_required
def explore(request):
    return render(request, 'explore.html')


@login_required
def chat(request):
    return render(request, 'index.html')


@login_required
def post(request):
    foods = FoodPost.objects.all().order_by('-created_at')

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        food_data = list(foods.values("id", "name", "location", "created_at", "photo"))
        for post_item in food_data:
            post_item["created_at"] = post_item["created_at"].isoformat()
        return JsonResponse({"foods": food_data})

    return render(request, "profile.html", {"foods": foods})


@login_required
def invite_member(request):
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.user = request.user
            invitation.save()

            send_mail(
                'You are invited to join our website!',
                'Please join us at our website: [URL]',
                'swapeatmail@gmail.com',
                [invitation.email],
                fail_silently=False,
            )
            return redirect('post')
    else:
        form = InvitationForm()

    return render(request, 'invite_member.html', {'form': form})


# ============================================================
# SEARCH
# ============================================================

def search_meals(request):
    meals = None
    query = ''
    if 'q' in request.GET:
        query = request.GET['q']
        meals = FoodPost.objects.filter(name__icontains=query)
    return render(request, 'search_meals.html', {'meals': meals, 'query': query})


@login_required
def notification(request):
    form = FoodPostForm()
    food_posts = list(FoodPost.objects.values("latitude", "longitude", "photo", "name", "radius", "location", "created_at", "id"))

    for post in food_posts:
        post["created_at"] = post["created_at"].isoformat()

    return render(request, "notification.html", {"form": form, "food_posts": json.dumps(food_posts)})


# ============================================================
# GEMINI CHATBOT API
# ============================================================

def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_question = data.get("question", "")

        gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

        payload = {"contents": [{"parts": [{"text": user_question}]}]}
        headers = {
            "Authorization": f"Bearer {settings.GEMINI_API_KEY}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(gemini_url, json=payload, headers=headers)
            if response.status_code == 200:
                gemini_response = response.json()
                answer = gemini_response.get("content", "Cannot generate response.")
            else:
                answer = f"Error: Status {response.status_code}"
        except Exception as e:
            answer = f"Error: {str(e)}"

        return JsonResponse({"answer": answer})

    return JsonResponse({"error": "Invalid request method."}, status=400)


# ============================================================
# CHAT ROOM
# ============================================================

@login_required
def CreateRoom(request):
    if request.method == 'POST':
        username = request.POST['username']
        room = request.POST['room']

        try:
            Room.objects.get(room_name=room)
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
        Message.objects.create(room=get_room, sender=username, message=message)

    get_messages = Message.objects.filter(room=get_room)

    return render(request, 'message.html', {
        "messages": get_messages,
        "user": username,
        "room_name": room_name,
    })
