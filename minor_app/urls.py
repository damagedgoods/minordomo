from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("message/<slug:slug>/", views.message, name="message"),
]
