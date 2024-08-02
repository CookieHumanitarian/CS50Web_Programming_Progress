from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Bids, Comments

class createListing(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField()
    start_Bid = forms.IntegerField()
    image = forms.CharField(required=False)
    
class bidForm(forms.Form):
    new_bid = forms.IntegerField()
    
class commentForm(forms.Form):
    comment = forms.CharField()

def index(request):
    all_listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": all_listings,
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def create(request):
    form = createListing()
    return render(request, "auctions/create.html", {
        "form": form
    })

def saveListing(request):
    if request.method == "POST":
        form = createListing(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            startBid = form.cleaned_data['start_Bid']
            image = form.cleaned_data['image']
            user = request.user
            instance = Listing(auctioneer = user, title=title, description=description, startBid=startBid, image=image)
            instance.save()
            
            bid = Bids(listing=instance, bidder=user, amount=startBid)
            bid.save()
            return HttpResponseRedirect(reverse("index"))
    
    else:
        form = createListing()

    return render(request, "auctions/create.html", {
        "form": form
    })
    
    
    
def item(request, title):
    data = Listing.objects.get(title=title)
    comment = Comments.objects.all()
    form = bidForm()
    user = request.user
    
    try:
        oldForm = Bids.objects.get(listing=data)
    except Bids.DoesNotExist:
        oldForm = None
    
    if request.method == "POST":
        newBid = bidForm(request.POST)
        if newBid.is_valid():
            newBidAmount = newBid.cleaned_data['new_bid']

            if oldForm:
                if newBidAmount == oldForm.amount:
                    messages.info(request, 'Invalid amount')
                else:
                    oldForm.amount = newBidAmount
                    oldForm.bidder = user
                    oldForm.save()                    
                    messages.info(request, 'New bidded added')

            else:
                Bids.objects.create(listing=data, bidder=user, amount=newBidAmount)

    
    return render(request, "auctions/item.html", {
        "data": data,
        "form": form,
        "bid": oldForm,
        "auctioneer": user
    })
    
def add_watchlist(request, title):
    data = Listing.objects.get(title=title)
    if data.watchlist == False:
        data.watchlist = True
        messages.info(request, 'Added to Watchlist')
    else:
        data.watchlist = False
        messages.info(request, 'Removed from Watchlist')

    data.save()
    
    return HttpResponseRedirect(reverse("index"))

def watchlist(request):
    all_listings = Listing.objects.all()
    return render(request, "auctions/watchlist.html", {
        "listings": all_listings,
    })
    
    
def close(request, title):
    data = Listing.objects.get(title=title)
    if data.open == True:
        data.open = False
        messages.info(request, 'Closed Auction')

    data.save()
    
    return HttpResponseRedirect(reverse("item", title))

def comment(request, title):
    data = Listing.objects.get(title=title)
    user = request.user
    
    if request.method == "POST":
        form = commentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            instance = Comments(listing=data, user=user, comment=comment)
            instance.save()
            
            return HttpResponseRedirect(reverse("index"))
        