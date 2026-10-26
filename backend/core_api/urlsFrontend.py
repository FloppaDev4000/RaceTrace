from django.urls import path
from core_api import views

urlpatterns = [
    path("demo/", views.demo, name="demo"),
    path("", views.home, name="home"),
    path("get-races/", views.callGetRaces, name="get-races"),
]