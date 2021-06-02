from django.db import models
import datetime
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from copy import deepcopy

# Create your models here.
class Prayer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='prayers',
        on_delete=models.CASCADE,
    )
    prayer_title = models.CharField(max_length=100)
    prayer_text = models.TextField(max_length=200)
    created_date = models.DateTimeField(
        'date created',
        auto_now_add=True,
    )
    last_prayed_date = models.DateTimeField(
        'date last prayed',
        auto_now_add=True,
    )
    expire_date = models.DateField(
        'date to expire',
        blank=True,
        null=True,
    )
    FREQUENCY_CHOICES = [
        (-1, 'Rotating'),
        (1, 'Daily'),
    ]
    frequency = models.IntegerField(
        choices=FREQUENCY_CHOICES,
        default=-1,
        )
    VISIBILITY_CHOICES = [
        (0, 'Private'),
        (1, 'Selective'),
        (2, 'Public'),
    ]
    visibility = models.IntegerField(
        choices=VISIBILITY_CHOICES,
        default=0,
    )
    visible_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='others_prayers',
    )
    reference_prayer = models.ForeignKey(
        "self",
        related_name="referenced_by",
        null=True,
        default=None,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.prayer_title

    def was_prayed_today(self):
        now=timezone.now();
        start_of_day=now.replace(hour=0, minute=0, second=0, microsecond=0)
        return self.last_prayed_date >= start_of_day

    def update_last_prayed(self):
        self.last_prayed_date=timezone.now()
        self.save()

    def get_absolute_url(self):
        # return reverse('prayer:detail', args=(self.id,))
        return reverse('prayer:index')

    def create_reference_prayer(self, user):
        p=deepcopy(self)
        p.pk=None
        p.reference_prayer=self
        p.user=user
        p.created_date=timezone.now()
        p.last_prayed_date=timezone.now()
        p.save()
        return p

class DailyPrayerList(models.Model):
    class Meta(object):
        unique_together = (("date", "user"), )

    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='daily_list',
                                on_delete=models.CASCADE)
    prayer = models.ManyToManyField(Prayer)
