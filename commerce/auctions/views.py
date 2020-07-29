from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
from .models import User, Listing, Comment, Bid

def index(request):
    listings = Listing.objects.all()
    for listing in listings:
        if len(listing.description) > 128:
            listing.description = listing.description[0:128] + "..."
    return render(request, "auctions/index.html",{
        "listings": listings
    })

@login_required  
def create_listing(request):
    if request.method == "POST":
        user = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        category = request.POST["category"]
        starting_bid = float(request.POST["starting bid"])
        image = request.POST["image"]
        date = datetime.datetime.now()
        listing = Listing(title=title,description=description,category=category,starting_bid=starting_bid,image=image,date=date,creator=user)
        listing.save()
    return render(request, "auctions/create_listing.html")


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
         user = request.user
         text = request.POST["text"]
         date = datetime.datetime.now()
         comment = Comment(date=date, user=user, text=text, listing=listing)
         comment.save()
    return render(request, "auctions/listing.html",{
        'listing':listing,
        'bids': listing.bids,
        'comments': listing.comments.all(),
        'subscribers': listing.subscribers.all()
    })

@login_required
def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        value = int(request.POST["bid"])
        last_bid = listing.bids.last()
        user = request.user
        date = datetime.datetime.now()
        bid = Bid(date=date, value=value, user=user, listing=listing)
        if last_bid is not None:
            if value > last_bid.value:
                bid.save()
        elif value > listing.starting_bid:
            bid.save()
    return HttpResponseRedirect(reverse('listing', args=[listing.id,]))

@login_required
def close(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        listing.status = False
        listing.save()
    return HttpResponseRedirect(reverse('index'))

@login_required
def subscribe(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        listing.subscribers.add(user)
    return HttpResponseRedirect(reverse('listing', args=[listing.id,]))

def unsubscribe(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        listing.subscribers.remove(user)
    return HttpResponseRedirect(reverse('listing', args=[listing.id,]))

def categories(request):
    listings = Listing.objects.all()
    categories = set()
    for listing in listings:
        if listing.category != "":
            categories.add(listing.category)
    return render(request, "auctions/categories.html",{
        'categories': categories
    })

def category(request, category):
    listings = Listing.objects.filter(category=category)
    for listing in listings:
        if len(listing.description) > 128:
            listing.description = listing.description[0:128] + "..."
    return render(request, "auctions/category.html",{
        'listings': listings
    })

@login_required
def watchlist(request):
    if request.user.is_authenticated:
        watchlist = request.user.watchlist.all()
        for listing in watchlist:
            if len(listing.description) > 128:
                listing.description = listing.description[0:128] + "..."
        return render(request, "auctions/watchlist.html",{
            'watchlist': watchlist
        })
    return HttpResponseRedirect(reverse("index"))   

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


@login_required
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