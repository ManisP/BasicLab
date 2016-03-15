from django.conf.urls import patterns, url
from lab import views


app_name = 'lab'
urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^submissions', views.LabIndex.as_view(), name='submissions'),
    url(r'^results', views.ResultIndex.as_view(), name='results'),
    url(r'^submissionresults/[0-9]+/(?P<pk>[0-9]+)', views.SubmissionResults, name='submissionresults'),
    url(r'^submissionindex/(?P<pk>[0-9]+)', views.SubmissionIndex.as_view(), name='submissionindex'),
    url(r'^createsubmission/(?P<pk>[0-9]+)', views.CreateSubmission, name='createsubmission'),
]
