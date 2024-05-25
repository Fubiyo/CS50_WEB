from django.urls import path

from . import views


app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("random", views.random_page, name="random"),
    path("entry", views.entry, name="entry"),
    path("edit", views.edit, name="edit"),
    path("saved", views.saved, name="saved"),
]
