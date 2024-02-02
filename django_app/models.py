from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# TODO: Realize Category and Tags for Post
# class Category(models.Model):
#     name = models.CharField(max_length=255)


# class Tag(models.Model):
#     name = models.CharField(max_length=255)


class Profile(models.Model):
    user = models.OneToOneField(
        verbose_name="User",
        blank=True,
        null=False,
        to=User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    name = models.CharField(
        verbose_name="Name",
        blank=True,
        null=False,
        max_length=100,
    )
    avatar = models.ImageField(
        verbose_name="Avatar",
        validators=[FileExtensionValidator(["jpg", "png", "jpeg", "svg"])],
        unique=False,
        editable=True,
        blank=False,
        null=False,
        default="profile/avatars/default.svg",
        upload_to="profile/avatars",
    )
    # TODO: Add Birth Date, Location and Bio fields

    class Meta:
        app_label = "auth"
        ordering = ("-user",)

    def __str__(self):
        return f"{self.user} - {self.name}"


@receiver(post_save, sender=User)
def profile_create(sender, instance, created, **kwargs):
    try:
        profile = Profile.objects.get(user=instance)
    except Exception:
        profile = Profile.objects.create(user=instance, name=instance.username)


class Post(models.Model):
    user = models.ForeignKey(
        verbose_name="User", to=User, on_delete=models.CASCADE, null=False, blank=True
    )
    # category = models.ForeignKey(
    #     verbose_name="Category", to=Category, on_delete=models.CASCADE
    # )
    # tags = models.ManyToManyField(verbose_name="Tags", to=Tag, on_delete=models.CASCADE)
    content = models.TextField(
        verbose_name="Content",
        blank=True,
        null=False,
    )
    image = models.ImageField(
        verbose_name="Image",
        validators=[FileExtensionValidator(["jpg", "png", "jpeg"])],
        upload_to="posts/image",
        null=True,
        blank=True,
    )
    creation_date = models.DateTimeField(
        verbose_name="Creation date", auto_now_add=True, null=False, blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.creation_date}"
