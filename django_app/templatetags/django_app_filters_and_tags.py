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
