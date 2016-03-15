from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
import datetime
# from django.utils.formats import get_format

# Create your models here.

class Lab(models.Model):
    lab_name = models.CharField(max_length=200)
    # my_formats = get_format('DATETIME_INPUT_FORMATS')
    pub_date = models.DateTimeField( 'date published', default = timezone.now)
    def __str__(self):
        return self.lab_name

    def format_date(self):
        return "%s" % format(self.pub_date, "%d-%M-%Y")

class Question(models.Model):
    lab = models.ForeignKey(Lab)
    prompt = models.CharField(max_length=200)
    trials = models.IntegerField(default=6)

    def get_trials(self):
        return self.trials;

class Variable(models.Model):
    question = models.ForeignKey(Question)
    variable_name = models.CharField(max_length=200)
    def __str__(self):
        return self.variable_name
    

class Submission(models.Model):
    lab = models.ForeignKey(Lab)
    w_number = models.CharField(max_length=10)

class RawData(models.Model):
    submission = models.ForeignKey(Submission)
    variable = models.ForeignKey(Variable)
    raw_data = models.DecimalField(decimal_places = 10, max_digits = 50)
