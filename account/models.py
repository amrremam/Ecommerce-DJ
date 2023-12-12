from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    rest_password_token = models.CharField(max_length=50, default=True, blank=True)
    reset_password_expire = models.DateTimeField(null=True, blank=True)


@receiver(post_save, sender=User)
def post_save(sender, instance, created, **kwargs):
    print('instance')
    user=instance

    if created:
        profile = Profile(user=user)
        profile.save()
