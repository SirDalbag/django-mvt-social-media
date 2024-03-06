from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.models import Q
from django_app import models


@login_required(login_url="sign-up")
def home(request):
    posts = models.Post.objects.all().order_by("-creation_date")
    if request.method == "GET":
        return render(request, "home.html", {"posts": posts})
    elif request.method == "POST":
        try:
            content = request.POST.get("content", None)
            image = request.FILES.get("image", None)
            if content or image:
                post = models.Post.objects.create(
                    user=request.user, content=content, image=image
                )
            else:
                raise Exception("Unable to send an empty post")
            return redirect("home")
        except Exception as error:
            return render(request, "home.html", {"posts": posts, "error": error})


@login_required(login_url="sign-up")
def post(request, id):
    post = models.Post.objects.get(id=id)
    comments = models.Comment.objects.filter(post=post).order_by("-creation_date")
    if request.method == "GET":
        return render(request, "post.html", {"post": post, "comments": comments})
    elif request.method == "POST":
        try:
            content = request.POST.get("content", None)
            image = request.FILES.get("image", None)
            if content or image:
                comment = models.Comment.objects.create(
                    user=request.user, post=post, content=content, image=image
                )
            else:
                raise Exception("Unable to send an empty comment")
            return redirect("post", id)
        except Exception as error:
            return render(
                request,
                "post.html",
                {"post": post, "comments": comments, "error": error},
            )


@login_required(login_url="sign-up")
def profile(request, username, type):
    user = User.objects.get(username=username)
    profile = models.Profile.objects.get(user=user)
    if type == "posts":
        content = models.Post.objects.filter(user=user).order_by("-creation_date")
    elif type == "replies":
        content = models.Comment.objects.filter(user=user).order_by("-creation_date")
    elif type == "likes":
        content = models.Post.objects.filter(like__user=user)
    return render(
        request, "profile.html", {"profile": profile, "content": content, "type": type}
    )


@login_required(login_url="sign-up")
def edit(request):
    profile = models.Profile.objects.get(user=request.user)
    if request.method == "GET":
        return render(request, "edit.html", {"profile": profile})
    elif request.method == "POST":
        try:
            name = request.POST.get("name", None)
            email = request.POST.get("email", None)
            location = request.POST.get("location", None)
            bio = request.POST.get("bio", None)
            avatar = request.FILES.get("avatar", None)
            if name and name != profile.name:
                profile.name = name
            if email and email != profile.user.email:
                profile.user.email = email
            if location and location != profile.location:
                profile.location = location
            if bio and bio != profile.bio:
                profile.bio = bio
            if avatar:
                profile.avatar = avatar
            profile.save()
            return redirect("profile", profile.user.username, "posts")
        except Exception as error:
            return render(request, "edit.html", {"profile": profile, "error": error})


@login_required(login_url="sign-up")
def search(request):
    search = request.GET.get("search", "")
    filter = request.GET.get("filter", "posts")
    profiles, posts = [], []
    if filter == "posts":
        posts = models.Post.objects.filter(content__icontains=search)
    elif filter == "users":
        profiles = models.Profile.objects.filter(
            Q(name__icontains=search) | Q(user__username__icontains=search)
        )
    return render(
        request,
        "search.html",
        {
            "profiles": profiles,
            "posts": posts,
            "search": search,
            "filter": filter,
        },
    )


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


@login_required(login_url="sign-up")
def like(request, id):
    post = models.Post.objects.get(id=id)
    like = models.Like.objects.filter(user=request.user, post=post)
    if like:
        like.delete()
    else:
        like = models.Like.objects.create(user=request.user, post=post)
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url="sign-up")
def follow(request, id):
    subcription = models.Subscription.objects.filter(
        follower=request.user, following=User.objects.get(id=id)
    )
    if subcription:
        subcription.delete()
    else:
        subcription = models.Subscription.objects.create(
            follower=request.user, following=User.objects.get(id=id)
        )
    return redirect(request.META.get("HTTP_REFERER", "/"))
