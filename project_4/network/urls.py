
from django.urls import path

from . import views

app_name = "network"

urlpatterns = [

    # python routes
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("all_posts", views.all_posts, name="all_posts"), 
    path("following", views.following, name="following"),
    path("new_post", views.new_post, name="new_post"),
    path("create_post", views.create_post, name="create_post"),


    # api routes
    path("likes", views.likes, name="likes")
    # path("edit", views.edit, name="edit")
]
