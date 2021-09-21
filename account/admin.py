from django.contrib import admin
from .models import Profile, AccountSettings

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth']

@admin.register(AccountSettings)
class AccountSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'daily_email', 'rotating_prayer_num', 'auto_pray']
