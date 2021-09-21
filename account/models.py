from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    following = models.ManyToManyField("self",
                                symmetrical=False,
                                blank=True,
                                related_name='followers')

    def __str__(self):
        return f'Profile for user {self.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class AccountSettings(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='settings',
        on_delete=models.CASCADE,
    )
    daily_email = models.BooleanField(default=False)
    rotating_prayer_num = models.IntegerField(
                                    default=3,
                                    validators=[MinValueValidator(0)],
                                    )
    auto_pray = models.BooleanField(default=False)

    def __str__(self):
        return f'Account settings for user {self.user.username}'

@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        AccountSettings.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_settings(sender, instance, **kwargs):
    instance.settings.save()
