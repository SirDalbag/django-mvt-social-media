from django.urls import path
from django_app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sign-up", views.sign_up, name="sign-up"),
    path("sign-in", views.sign_in, name="sign-in"),
    path("sign-out", views.sign_out, name="sign-out"),
    path("post/<id>", views.post, name="post"),
    path("like/<id>", views.like, name="like"),
]
