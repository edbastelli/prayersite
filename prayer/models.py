from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class Prayer(models.Model):
    prayer_title = models.CharField(max_length=100)
    prayer_text = models.CharField(max_length=200)
    created_date = models.DateTimeField('date created')
    last_prayed_date = models.DateTimeField('date last prayed')
    frequency = models.IntegerField()

    def __str__(self):
        return self.prayer_title

    def was_prayed_today(self):
        now=timezone.now();
        start_of_day=now.replace(hour=0, minute=0, second=0, microsecond=0)
        return self.last_prayed_date >= start_of_day

    def update_last_prayed(self):
        self.last_prayed_date=timezone.now()
        self.save()
