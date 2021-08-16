from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Listing, Bid

# Register your models here.


class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_closed', 'category', 'bid')


class BidAdmin(admin.ModelAdmin):
    list_display = ('bid', 'user')


admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
