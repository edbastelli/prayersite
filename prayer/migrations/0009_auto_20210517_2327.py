# Generated by Django 3.2 on 2021-05-18 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prayer', '0008_auto_20210517_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyprayerlist',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='prayer',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
