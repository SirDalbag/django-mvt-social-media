from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# TODO: Realize Category and Tags for Post


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
    birth_date = models.DateField(
        verbose_name="Birth Date",
        blank=False,
        null=True,
    )
    location = models.CharField(
        verbose_name="Location",
        blank=False,
        null=True,
        max_length=100,
    )
    bio = models.TextField(
        verbose_name="Bio",
        blank=False,
        null=True,
        max_length=150,
    )

    class Meta:
        app_label = "auth"
        ordering = ("-user",)
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

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
    content = models.TextField(
        verbose_name="Content",
        blank=False,
        null=True,
        max_length=255,
    )
    image = models.ImageField(
        verbose_name="Image",
        validators=[FileExtensionValidator(["jpg", "png", "jpeg"])],
        upload_to="posts/image",
        null=True,
        blank=False,
    )
    creation_date = models.DateTimeField(
        verbose_name="Creation date", auto_now_add=True, null=False, blank=True
    )

    class Meta:
        app_label = "django_app"
        ordering = ("-creation_date",)
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.user.username} - {self.creation_date}"

    def likes_count(self):
        return Like.objects.filter(post=self).count()

    def comments_count(self):
        return Comment.objects.filter(post=self).count()


class Like(models.Model):
    user = models.ForeignKey(
        verbose_name="User", to=User, on_delete=models.CASCADE, null=False, blank=True
    )
    post = models.ForeignKey(
        verbose_name="Post", to=Post, on_delete=models.CASCADE, null=False, blank=True
    )

    class Meta:
        app_label = "django_app"
        verbose_name = "Like"
        verbose_name_plural = "Likes"

    def __str__(self):
        return f"{self.user.username} - {self.post}"


class Comment(models.Model):
    user = models.ForeignKey(
        verbose_name="User", to=User, on_delete=models.CASCADE, null=False, blank=True
    )
    post = models.ForeignKey(
        verbose_name="Post", to=Post, on_delete=models.CASCADE, null=False, blank=True
    )
    content = models.TextField(
        verbose_name="Content",
        blank=False,
        null=True,
        max_length=255,
    )
    image = models.ImageField(
        verbose_name="Image",
        validators=[FileExtensionValidator(["jpg", "png", "jpeg"])],
        upload_to="comments/image",
        null=True,
        blank=False,
    )
    creation_date = models.DateTimeField(
        verbose_name="Creation date", auto_now_add=True, null=False, blank=True
    )

    class Meta:
        app_label = "django_app"
        ordering = ("-creation_date",)
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"{self.user.username} - {self.post}"
