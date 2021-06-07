from django import template
from datetime import datetime
from prayer.models import Prayer

register = template.Library()

@register.filter
def dateof(date_time):
    return datetime.date(date_time)

@register.filter
def getall(queryset):
    return queryset.all()

@register.filter
def displayFrequency(prayer):
    return prayer.get_frequency_display()

@register.filter
def expireDate(prayer):
    if prayer.expire_date:
        return prayer.expire_date
    else:
        return "Never"
