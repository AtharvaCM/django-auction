from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path("display_category", views.display_category, name="display_category"),

]
