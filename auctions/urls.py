from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path("<int:listing_id>", views.display_listing, name="display_listing"),
    path("display_category", views.display_category, name="display_category"),

]
