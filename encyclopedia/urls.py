from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_page", views.add_page, name="add_page"),
    path("edit_page", views.edit_page, name="edit_page"),
    path("random_page", views.random_page, name="random_page"),
    path("<str:page>", views.pages, name="pages")

    
]
