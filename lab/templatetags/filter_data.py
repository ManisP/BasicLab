from django.template import Library
from lab.models import RawData

register = Library()

@register.filter
def filter_data(rawdata, submission):
    return rawdata.filter(submission=submission)
