import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def newPost (request):
    if request.method == "POST":
        # Get content of body
        data = json.loads(request.body)
        body = data.get("body", "")
        
        # Save content to model
        post = Post(
            user = request.user,
            body=body,
        )
        post.save()
        
        return JsonResponse({"message": "Post made successfully."}, status=201)
    
@login_required
def allPosts(request):
    if request.method == 'GET':
        
        # Get in reverse chronology order
        posts = Post.objects.all().order_by("-timestamp").all()
        
        # Return posts in reverse chronology order
        return JsonResponse([post.serialize() for post in posts], safe=False)

@login_required
def profile(request, user):
    data = Post.objects.filter(user__username=user)
    return render(request, "network/profile.html", {
        "data": data
    })