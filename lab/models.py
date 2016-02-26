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


# Works up to this point
# ----------------------------------------------------------------------------
# Anything under here is being tested
class testLab(models.Model):
    lab_name = models.CharField(max_length=200)
    def __str__(self):
        return self.lab_name

class testQuestion(models.Model):
    test_lab = models.ForeignKey(testLab)
    question_name = models.CharField(max_length=200)
    question_prompt = models.CharField(max_length=200)
    def __str__(self):
        return self.question_name




class BigLab(models.Model):
    lab_name = models.CharField(max_length=200)
    number_of_question = models.IntegerField(default = 0)
    pub_date = models.DateTimeField('date published', default = timezone.now)

    def __str__(self):
        return self.lab_name


class Question(models.Model):
    bigLab = models.ForeignKey(BigLab)
    prompt = models.CharField(max_length=200)
    number_of_variables = models.IntegerField()
    number_of_trials = models.IntegerField()
    def __str__(self):
        return self.prompt


class Variable(models.Model):
    question = models.ForeignKey(Question)
    variable_name = models.CharField(max_length=20)
    trials = models.IntegerField()
    def __str__(self):
        return self.prompt


class DataValues(models.Model):
    variable = models.ForeignKey(Variable)
    data = models.FloatField()
    def __str__(self):
        return str(self.data)
