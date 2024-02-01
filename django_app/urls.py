from django.urls import path
from django_app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sign-up", views.sign_up, name="sign-up"),
    path("sign-in", views.sign_in, name="sign-in"),
]
