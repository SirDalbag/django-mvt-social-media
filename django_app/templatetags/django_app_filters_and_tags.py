from django import template
from django_app import models

register = template.Library()


@register.filter(name="has_like")
def has_like(post, user):
    return models.Like.objects.filter(post=post, user=user).exists()
