from django import template
from django_app import models

register = template.Library()


@register.filter(name="short")
def short(text):
    if len(text) > 35:
        return text[:35] + "..."
    else:
        return text


@register.filter(name="has_like")
def has_like(post, user):
    return models.Like.objects.filter(post=post, user=user).exists()


@register.filter(name="is_following")
def is_following(user, other_user):
    return not models.Subscription.objects.filter(
        follower=user, following=other_user
    ).exists()
