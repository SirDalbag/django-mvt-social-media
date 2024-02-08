from django.contrib import admin
from django_app import models

admin.site.register(models.Profile)
admin.site.register(models.Post)
admin.site.register(models.Like)
admin.site.register(models.Comment)
