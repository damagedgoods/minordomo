from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    #path("collection/new/", views.new, name="new_collection"),
]
