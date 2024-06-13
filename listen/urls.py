from . import views
from django.urls import path


urlpatterns = [
    path("ping/", views.ping, name="ping"),
    path("save/", views.save, name="save"),
    path("index/", views.index, name="index"),
]