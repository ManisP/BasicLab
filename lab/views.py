from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic
from lab.forms import BasicLabForm, CreateALab, CreateASubmission
from lab.models import Lab, Submission
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

# Static HTML pages used for user movement
class Thanks(generic.TemplateView):
    template_name = 'lab/thanks.html'

class Index(generic.TemplateView):
    template_name = 'lab/index.html'
# ---------------------------------------

# Displays lab options, directs to a submission for that lab
class LabIndex(generic.ListView):
    template_name = 'lab/labindex.html'
    context_object_name = 'lab_list'

    # All the labs that it will be listing
    def get_queryset(self):
        return Lab.objects.all()

# Same as LabIndex, but directs them to the already made submissions
class SubmissionIndex(generic.ListView):
    model = Lab
    template_name = 'lab/submissionindex.html'
    context_object_name = 'lab_list'

    # All the labs that it will be listing
    def get_queryset(self):
        return Lab.objects.all()

# Links to the page that allows users to create labs
class CreateLab(generic.CreateView):
    template_name = 'lab/createlab.html'
    model = Lab
    fields = ['lab_name', 'lab_question']

    # Basic redirect
    def get_success_url(self):
        return reverse('lab:thanks')

# Links to the page that allows users to submit lab submissions
class CreateSubmission(generic.CreateView):
    template_name = 'lab/createsubmission.html'
    model = Submission
    fields = ['student_name', 'student_email', 'input_int']

    # Used to get the lab object into the page, so we can display questions from it
    def get_context_data(self, **kwargs):
        context = {}
        context['lab'] = get_object_or_404(Lab, pk=self.kwargs['pk'])
        return super(generic.CreateView, self).get_context_data(**context)

    # Ensures all the forms fields are valid. Also links up the foreign key to the parent lab
    def form_valid(self, form):
        form.instance.lab = get_object_or_404(Lab, pk=self.kwargs['pk'])
        return super(CreateSubmission, self).form_valid(form)

    # Basic redirect
    def get_success_url(self):
        return reverse('lab:thanks')

# Displays all the submissions of one lab
class SubmissionView(generic.ListView):
    print "running the main"
    template_name = 'lab/submissionview.html'
    context_object_name = 'submission_list'

    # Gets all of the submissions to display
    def get_queryset(self, **kwargs):
        lab = get_object_or_404(Lab, pk=self.kwargs['pk'])
        return lab.submission_set.all()

    # Loads in the lab to the context, used to print lab info
    def get_context_data(self, **kwargs):
        context = {}
        lab = get_object_or_404(Lab, pk=self.kwargs['pk'])
        context['lab'] = lab
        return super(generic.ListView, self).get_context_data(**context)

# Works up to this point
# ----------------------------------------------------------------------------#



































    # def get_queryset(self):
    #     return Lab.objects.order_by('pub_date')[:5]
