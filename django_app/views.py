from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_app import models


@login_required(login_url="sign-up")
def home(request):
    posts = models.Post.objects.all().order_by("-creation_date")
    return render(request, "home.html", {"posts": posts})


def sign_up(request):
    return render(request, "sign-up.html")


def sign_in(request):
    return render(request, "sign-in.html")
