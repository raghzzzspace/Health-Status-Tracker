# Generated by Django 5.0.2 on 2024-04-16 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WellWatchin', '0017_signup_user_alter_signup_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
