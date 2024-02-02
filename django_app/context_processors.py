from django_app import models


def profile(request):
    if request.user.is_authenticated:
        profile = models.Profile.objects.get(user=request.user)
    else:
        profile = None
    return {"profile": profile}
