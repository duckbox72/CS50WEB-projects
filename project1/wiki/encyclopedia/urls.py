from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("addentry", views.addentry, name="addentry"),
    path("editentry", views.editentry, name="editentry"),
    path("random", views.random, name="random"),
    path("<str:name>", views.entry, name="entry"),
    
]
