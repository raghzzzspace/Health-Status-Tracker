# Generated by Django 5.0.2 on 2024-04-16 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WellWatchin', '0005_alter_signup_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='username',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
