from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from datetime import date
# from datetime import time


class Question(models.Model):
    query = models.CharField(max_length=50)
    answer = models.CharField(max_length=500)


class Calendar(models.Model):
    date_start = models.DateField(default=date.today)
    date_end = models.DateField(default=date.today)
    event = models.CharField(max_length=1000, default="")
    remark = models.CharField(max_length=500)
    name= models.CharField(max_length=500, default="No event name")
    color= models.CharField(max_length=100, default= "#004980")


class Course(models.Model):
    course = models.CharField(max_length=500)
    college = models.CharField(max_length=500)
    college_acronym = models.CharField(max_length=100, default='unavailable')
    campus = ArrayField(models.CharField(max_length=50), blank=True)


class Contact(models.Model):
    office_name = models.CharField(max_length=1000)
    email = models.EmailField(max_length = 5000, blank=True)
    facebook = models.URLField(max_length = 2000, blank=True)
    landline = models.CharField(max_length = 500, blank=True)
    college_secretary = models.CharField(max_length = 500, blank=True)
    ref = models.CharField(max_length = 500, blank=True)


class userIntent(models.Model):
    intent = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Executive(models.Model):
    position = models.CharField(max_length=250)
    name = models.CharField(max_length=500)


class Dean(models.Model):
    college = models.CharField(max_length=250)
    name = models.CharField(max_length=500)


class Population(models.Model):
    college = models.CharField(max_length=250)
    student_population = models.IntegerField(default=0)


class Random(models.Model):
    key = models.CharField(max_length=500)
    question = models.CharField(max_length=2000, default="")
    answer = models.CharField(max_length=2000)


class Action(models.Model):
    action = models.CharField(max_length=150)
    date = models.DateField(default=date.today)
    time = models.TimeField(auto_now_add=True)


class ChatbotSettings(models.Model):
    key = models.CharField(max_length=150)
    message = models.CharField(max_length=150, default="")
    is_disable = models.BooleanField(max_length=150, default=False)


class BetaTest(models.Model):
    message = models.CharField(max_length=1000)
    accuracy = models.CharField(max_length=100)
