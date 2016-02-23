from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Lab(models.Model):
    lab_name = models.CharField(max_length=200)
    lab_question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default = timezone.now)

    def __str__(self):
        return self.lab_name

class Submission(models.Model):
    lab = models.ForeignKey(Lab)
    student_name = models.CharField(max_length=200)
    student_email = models.EmailField(max_length=254)
    input_int = models.IntegerField()
    def __str__(self):
        return self.student_name
