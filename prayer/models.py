from django.db import models
import datetime
from django.utils import timezone
from django.conf import settings

# Create your models here.
class Prayer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='prayers',
                             on_delete=models.CASCADE)
    prayer_title = models.CharField(max_length=100)
    prayer_text = models.TextField(max_length=200)
    created_date = models.DateTimeField('date created',
                                        auto_now_add=True)
    last_prayed_date = models.DateTimeField('date last prayed',
                                            auto_now_add=True)
    expire_date = models.DateTimeField('date to expire',
                                       blank=True,
                                       null=True)
    frequency = models.IntegerField(default=-1)

    def __str__(self):
        return self.prayer_title

    def was_prayed_today(self):
        now=timezone.now();
        start_of_day=now.replace(hour=0, minute=0, second=0, microsecond=0)
        return self.last_prayed_date >= start_of_day

    def update_last_prayed(self):
        self.last_prayed_date=timezone.now()
        self.save()
