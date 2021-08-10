from django.shortcuts import render
from .models import Listing

# Create your views here.


def index(request):
    # listings = Listing.objects.filter(is_closed=False)
    template_name = 'auctions/index.html'
    context = {
        # "listings": listings,
    }
    return render(request, template_name, context)


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
