import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by("-timestamp").all()
    
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    
    return render(request, "network/index.html",{
        "page_obj": page_obj
    })


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

def profileView(request, user):
    posts = Post.objects.filter(user__username = user).order_by("-timestamp").all()
    
    try:
        currentUser = get_object_or_404(User, username=request.user)
        # Get following list for current user
        followingList = currentUser.following.split(",")
    except:
        currentUser = "Guest"
        followingList = "None"

    user = get_object_or_404(User, username=user)
    
    return render(request, "network/profile.html",{
        "posts": posts,
        "Profileuser": user,
        "currentUser": currentUser,
        "followingList": followingList
    })

def followView(request, profileUsername, currentUsername):
    
    currentUser = get_object_or_404(User, username=currentUsername)
    
    # Check to see if user is already following someone
    if currentUser.following:
        followingList = currentUser.following.split(',')
    else:
        followingList = []
        
    # Follow / unfollow function
    if profileUsername in followingList:
        followingList.remove(profileUsername)  
    else: 
        followingList.append(profileUsername)
    
    currentUser.following = ','.join(followingList)
    currentUser.save()
    
    return HttpResponseRedirect(reverse("index"))

def followPage(request):
    currentUser = get_object_or_404(User, username=request.user.username)
    currentFollowing = currentUser.following
    
    #Put all followers post into a list 
    posts = []
    
    for f in currentFollowing:
        follow = Post.objects.filter(user__username = f)
        posts.extend(follow)
    
    # Sort all posts in descending order
    posts = sorted(posts, key=lambda post: post.timestamp, reverse=True)
    
    return render(request, "network/following.html",{
        "posts": posts
    })