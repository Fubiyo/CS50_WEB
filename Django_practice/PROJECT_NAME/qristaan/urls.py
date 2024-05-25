from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("qristaan", views.qristaan, name="qristaan"),
    path("<str:namae>", views.greet, name="greet"),
]