from django.shortcuts import render, redirect
from .models import Listing, User, Bid
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Q

# Create your views here.


def index(request):
    listings = Listing.objects.filter(is_closed=False)[:2]
    template_name = 'auctions/index.html'
    context = {
        "listings": listings,
    }
    return render(request, template_name, context)


def login_view(request):
    if request.user.is_authenticated:
        # redirect to homepage
        return redirect('index')
    else:
        if request.method == 'POST':
            if request.user.is_authenticated:
                # redirect to homepage
                print("ala re aat")
                return render(request, 'auctions/index.html')
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
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse("index"))
    else:
        return redirect('index')


def register(request):
    if request.user.is_authenticated:
        # redirect to homepage
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            first_name = request.POST['fname']
            last_name = request.POST['lname']
            email = request.POST['email']
            phone = request.POST['phone']
            address = request.POST['address']
            age = request.POST['age']

            # Ensure password matches confirmation
            password = request.POST['password']
            confirmation = request.POST['confirmation']
            if password != confirmation:
                return render(request, 'auctions/register.html', {
                    'message': 'Passwords must match!'
                })

            print(first_name, last_name, phone, address, age)

            # Attempt to create new user
            try:
                user = User.objects.create_user(
                    username, email, password, first_name=first_name, last_name=last_name, phone=phone, address=address, age=age)
                print('create user called')
                user.save()
            except IntegrityError:
                return render(request, 'auctions/register.html', {
                    'message': 'Username already exists'
                })
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            print('nahi hote rav')
            return render(request, 'auctions/register.html')


def profile(request):
    template_name = 'auctions/profile.html'
    context = {}
    return render(request, template_name, context)
# ------------------------------------------------------------------------------------------------------------------


class SearchResultsView(ListView):
    # https://learndjango.com/tutorials/django-search-tutorial
    model = Listing
    template_name = 'auctions/search_results.html'
    # queryset = Listing.objects.filter(title__icontains='chevy')

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Listing.objects.filter(
            Q(title__icontains=query) | Q(category__icontains=query)
        )
        return object_list


def about(request):
    template_name = 'auctions/about.html'
    context = {}
    return render(request, template_name, context)


def help(request):
    template_name = 'auctions/enquiry.html'
    context = {}
    return render(request, template_name, context)


def terms(request):
    template_name = 'auctions/terms.html'
    context = {}
    return render(request, template_name, context)


def display_category(request):
    all_listings = Listing.objects.order_by().values_list(
        'category', flat=True).distinct()
    print(all_listings)

    if request.method == 'GET':
        listings = Listing.objects.filter(is_closed=False)
        context = {
            "listings": listings,
            "all_listings": all_listings,
        }
        return render(request, "auctions/display_category.html", context)

    category = request.POST.get('category', False)
    if category == 'All Categories':
        listings = Listing.objects.filter(is_closed=False)
    else:
        listings = Listing.objects.filter(category=category)

    listings = set(listings)
    context = {
        "listings": listings,
        "all_listings": all_listings,
    }
    return render(request, "auctions/display_category.html", context)


def display_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    # is_listing_in_watchlist = request.user in listing.watchlist.all()
    is_owner = request.user.username == listing.owner.username
    context = {
        "listing": listing,
        # "is_listing_in_watchlist": is_listing_in_watchlist,
        "is_owner": is_owner,
        # "comments": comments
    }
    return render(request, "auctions/listing_page.html", context)


def closed_listings(request):
    closed_listing = Listing.objects.filter(is_closed=True)
    context = {
        "listings": closed_listing,
    }
    template_name = 'auctions/closed_listings.html'
    return render(request, template_name, context)


def create_listing(request):
    template_name = 'auctions/create_listing.html'
    if request.method == "POST":
        user = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        category = request.POST['category']

        try:
            # Create new bid
            bid = Bid(bid=int(request.POST["bid"]), user=user)
            bid.save()

            # Create new listing
            listing = Listing(title=title, category=category, owner=user,
                              is_closed=False, description=description, bid=bid, url=image_url)
            listing.save()
            message_success = 'Successfully created listing'
            context = {
                'message_success': message_success,
            }
        except:
            message_danger = 'Cannot create listing!'
            context = {
                'message_danger': message_danger,
            }
        # return HttpResponseRedirect(reverse("index"))
        return render(request, template_name, context)
    else:
        return render(request, template_name)


def new_bid(request, listing_id):
    # you have to use online imgs to render it properly
    listing = Listing.objects.get(pk=listing_id)
    current_bid = listing.bid.bid
    new_bid = bid = int(request.POST["bid"])
    if new_bid > current_bid:
        updated_bid = Bid(bid=new_bid, user=request.user)
        updated_bid.save()
        listing.bid = updated_bid
        listing.save()
        context = {
            "listing": listing,
            "message": "Bid was updated successfully",
            "updated": True,
        }
        print('---------', listing.url)
        return render(request, "auctions/listing_page.html", context)
    else:
        context = {
            "listing": listing,
            "message": "Bid was updated successfully",
            "updated": True,
        }
        return render(request, "auctions/listing_page.html", context)


def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.is_closed = True
    listing.save()
    return HttpResponseRedirect(reverse("display_listing", args=(listing_id, )))
