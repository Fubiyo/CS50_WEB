from django.urls import path
from . import views

app_name = 'auctions'

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("register", views.register, name="register"),
    path("listings/<int:id>", views.listings, name="listings"),
    path("success", views.success, name="success"),
    path("fail", views.fail, name="fail")
]
