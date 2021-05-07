from django import template
from datetime import datetime

register = template.Library()

@register.filter
def dateof(date_time):
    return datetime.date(date_time)

@register.filter
def getall(queryset):
    return queryset.all()
