from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class Question(models.Model):
    query = models.CharField(max_length=50)
    answer = models.CharField(max_length=500)


class Calendar(models.Model):
    date_start = models.DateField()
    date_end = models.DateField()
    remark = models.CharField(max_length=500)


class Course(models.Model):
    course = models.CharField(max_length=500)
    college = models.CharField(max_length=500)
    college_acronym = models.CharField(max_length=100, default='unavailable')
    campus = models.CharField(max_length=500)


class userIntent(models.Model):
    intent = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
