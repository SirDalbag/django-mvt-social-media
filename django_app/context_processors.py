from django.contrib.auth.models import User
from django_app import models


def profile(request):
    profile = (
        models.Profile.objects.get(user=request.user)
        if request.user.is_authenticated
        else None
    )
    return {"profile": profile}


def popular_users(request):
    users = User.objects.all()
    popular_users = []
    for user in users:
        posts = models.Post.objects.filter(user=user)
        likes = sum(post.likes_count() for post in posts)
        popular_users.append({"user": user, "posts": len(posts), "likes": likes})
    popular_users = sorted(
        popular_users, key=lambda x: (x["likes"], x["posts"]), reverse=True
    )[:5]
    return {"popular_users": popular_users}
