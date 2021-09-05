from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),

    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('about', views.about, name='about'),
    path('help', views.help, name='help_and_support'),
    path('terms', views.terms, name='terms'),

    path('display_category', views.display_category, name='display_category'),
    path('<int:listing_id>', views.display_listing, name='display_listing'),

    path("closed_listings", views.closed_listings, name="closed_listings"),
    path("create_listing", views.create_listing, name="create_listing"),

    path("<int:listing_id>/new_bid", views.new_bid, name="new_bid"),
    path("<int:listing_id>/close_auction",
         views.close_auction, name="close_auction"),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
