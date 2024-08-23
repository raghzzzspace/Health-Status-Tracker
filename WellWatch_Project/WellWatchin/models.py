from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class SignUp(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField(max_length=50)
    username=models.CharField(default=None,max_length=20)
    password=models.CharField(default=None,max_length=10)
    age=models.IntegerField()
    gender=models.CharField(default='M/F',max_length=10)
    height=models.FloatField(max_length=4)
    weight=models.FloatField(max_length=4)
    bloodgroup=models.CharField(default=None,max_length=4)
    class Meta:
        db_table = 'wellwatchin_signup'

class Profile(models.Model):
    username=models.CharField(default=None,max_length=20)
    address=models.CharField(max_length=50)
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    country=models.CharField(max_length=20)
    postalcode=models.IntegerField()
    phone=models.BigIntegerField()
    extra=models.CharField(max_length=50)
    feedback=models.CharField(max_length=40)
    class Meta:
        db_table = 'wellwatchin_profile'

class Exercise(models.Model):
    username=models.CharField(default=None,max_length=20)
    duration=models.FloatField()
    date=models.DateField()

class BP(models.Model):
    username=models.CharField(default=None,max_length=20)
    sbp=models.CharField(max_length=4)
    dbp=models.CharField(max_length=4)

class Water(models.Model):
    username=models.CharField(default=None,max_length=20)
    quantity=models.IntegerField()
    date=models.DateField()
    
    
class Weight(models.Model):
    username=models.CharField(default=None,max_length=20)
    weight=models.IntegerField()
    date=models.DateField()
  
    
class Sleep(models.Model):
    username=models.CharField(default=None,max_length=20)
    sleep=models.IntegerField()
    date=models.DateField()
    