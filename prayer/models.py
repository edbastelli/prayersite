from django.db import models

# Create your models here.
class Prayer(models.Model):
    prayer_title = models.CharField(max_length=100)
    prayer_text = models.CharField(max_length=200)
    created_date = models.DateTimeField('date created')
    last_prayed_date = models.DateTimeField('date last prayed')
    frequency = models.IntegerField()
