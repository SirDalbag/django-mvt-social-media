from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django_app import models


@login_required(login_url="sign-up")
def home(request):
    posts = models.Post.objects.all().order_by("-creation_date")
    return render(request, "home.html", {"posts": posts})


def sign_up(request):
    if request.method == "POST":
        try:
            username = request.POST["username"]
            password = request.POST["password"]
            email = request.POST["email"]
            user = authenticate(username=username, password=password, email=email)
            if not user:
                name = request.POST.get("name")
                user = User.objects.create(
                    username=username, password=make_password(password), email=email
                )
                profile = models.Profile.objects.get(user=user)
                profile.name = name
                profile.save()
                login(request, user)
                return redirect("home")
        except Exception as error:
            return render(
                request,
                "sign-up.html",
                {"error": error},
            )
    return render(request, "sign-up.html")


def sign_in(request):
    if request.method == "POST":
        try:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if not user:
                raise Exception("Incorrect password, email or username")
            login(request, user)
            return redirect("home")
        except Exception as error:
            return render(
                request,
                "sign-in.html",
                {"error": error},
            )
    return render(request, "sign-in.html")


def sign_out(request):
    logout(request)
    return redirect("sign-in")
