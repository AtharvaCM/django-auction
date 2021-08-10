from django.shortcuts import render
from .models import Listing, User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.urls import reverse

# Create your views here.


def index(request):
    # listings = Listing.objects.filter(is_closed=False)
    template_name = 'auctions/index.html'
    context = {
        # "listings": listings,
    }
    return render(request, template_name, context)


def login_view(request):
    if request.method == 'POST':
        # attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # check if authentication is successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'auctions/login.html', {'message': 'Invalid Username or Password'})
    else:
        return render(request, 'auctions/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'auctions/register.html', {
                'message': 'Passwords must match!'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'auctions/register.html', {
                'message': 'Username already exists'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/register.html')

# ------------------------------------------------------------------------------------------------------------------


def display_category(request):
    category = request.POST.get('category', False)
    if category == False:
        listings = Listing.objects.filter(is_closed=False)
    else:
        listings = Listing.objects.filter(category=category)
        listings = set(listings)
    context = {
        "listings": listings,
    }
    return render(request, "auctions/listing_category.html", context)


def display_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    # is_listing_in_watchlist = request.user in listing.watchlist.all()
    # comments = listing.comments.all()
    is_owner = request.user.username == listing.owner.usernames
    context = {
        "listing": listing,
        # "is_listing_in_watchlist": is_listing_in_watchlist,
        "is_owner": is_owner,
        # "comments": comments
    }
    return render(request, "auctions/listing_page.html", context)


def about(request):
    template_name = 'auctions/about.html'
    context = {}
    return render(request, template_name, context)
