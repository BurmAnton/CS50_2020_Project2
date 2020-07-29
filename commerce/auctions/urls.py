from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/bid", views.bid, name="bid"),
    path("listing/<int:listing_id>/close", views.close, name="close"),
    path("listing/<int:listing_id>/subscribe", views.subscribe, name="subscribe"),
    path("listing/<int:listing_id>/unsubscribe", views.unsubscribe, name="unsubscribe"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/listing", views.create_listing, name="create listing")
]
