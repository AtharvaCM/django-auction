from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),

    path('about', views.about, name='about'),
    path('<int:listing_id>', views.display_listing, name='display_listing'),
    path('display_category', views.display_category, name='display_category'),

]

urlpatterns += staticfiles_urlpatterns()
