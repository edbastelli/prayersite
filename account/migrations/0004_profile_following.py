# Generated by Django 3.2 on 2021-05-29 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_profile_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(related_name='_account_profile_following_+', to='account.Profile'),
        ),
    ]
