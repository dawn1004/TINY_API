from django.db import models


class Question(models.Model):
    query = models.CharField(max_length=50)
    answer = models.CharField(max_length=500)


class Calendar(models.Model):
    date_start = models.DateField()
    date_end = models.DateField()
    remark = models.CharField(max_length=500)
