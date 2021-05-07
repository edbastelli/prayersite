# Generated by Django 3.2 on 2021-05-04 02:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prayer', '0004_alter_prayer_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyPrayerList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('prayer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prayer.prayer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='daily_list', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('date', 'user')},
            },
        ),
    ]
