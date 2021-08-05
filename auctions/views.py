from django.shortcuts import render
from .models import Listing

# Create your views here.


def index(request):
    listings = Listing.objects.filter(is_closed=False)
    template_name = 'auctions/index.html'
    context = {
        "listings": listings,
    }
    return render(request, template_name, context)


def display_category(request):
    category = request.POST["category"]
    listings = Listing.objects.filter(category=category)
    listings = set(listings)
    context = {
        "listings": listings,
    }
    return render(request, "auctions/index.html", context)
