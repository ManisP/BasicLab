from django.conf.urls import patterns, url
from lab import views


app_name = 'lab'
urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^submissions', views.SubmissionsIndex.as_view(), name='submissions'),
    url(r'^createsubmission/(?P<pk>[0-9]+)', views.CreateSubmission, name='createsubmission'),


    # url(r'^thanks', views.Thanks.as_view(), name='thanks'),
    # url(r'^createlab', views.CreateLab.as_view(), name='createlab'),
    # url(r'^createbiglab', views.addQuestionsToLab, name='createbiglab'),
    # url(r'^labindex', views.LabIndex.as_view(), name='labindex'),
    # url(r'^submissionindex', views.SubmissionIndex.as_view(), name='submissionindex'),
    # url(r'^createsubmission/(?P<pk>[0-9]+)', views.CreateSubmission.as_view(), name='createsubmission'),
    # url(r'^submissionview/(?P<pk>[0-9]+)', views.SubmissionView.as_view(), name='submissionview'),
]
