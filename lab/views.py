from django.shortcuts import get_object_or_404, render, render_to_response
from django.views import generic
from django.template import RequestContext
from lab.forms import BigLabForm, QuestionForm
from lab.forms import BasicLabForm, CreateALab, CreateASubmission
from lab.models import Lab, Submission, BigLab, Question, Variable, DataValues, testQuestion, testLab
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django import forms
from django.db import models


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import IntegrityError, transaction
from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render
from lab.forms import testQuestionForm, BaseTestQuestionFormSet, testLabForm

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
    def get_success_prompt(self):
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
    def get_success_prompt(self):
        return reverse('lab:thanks')

# Displays all the submissions of one lab
class SubmissionView(generic.ListView):
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
# ----------------------------------------------------------------------------
# Anything under here is being tested

# Creates a basic BigLab, need to work on this
# class CreateBigLab(generic.CreateView):
#     template_name = 'lab/createbiglab.html'
#     model = BigLab
#     fields = ['lab_name']
#
#     # Basic redirect
#     def get_success_prompt(self):
#         return reverse('lab:thanks')

def CreateBigLab(request):
    if request.method == "POST":
        print "POST"
        context = RequestContext(request)
        if request.POST.get("more_questions"):
            question_forms = []
            for i in range(0,context['big_lab_form'].get('number_of_question')):
                question_forms.append(QuestionForm)
            context['question_forms'] = question_forms
        return render_to_response('lab/createbiglab.html', context)

    else:
        print "GET"
        # Fill the context
        context = RequestContext(request)
        big_lab_form = BigLabForm()
        context['big_lab_form'] = big_lab_form

        question_forms = []
        for i in range(0, 3):
            question_forms.append(QuestionForm)
        context['question_forms'] = question_forms
    return render_to_response('lab/createbiglab.html', context)



# def CreateBigLab(request):
#     template_name = 'lab/createbiglab.html'
#     model = BigLab
#     fields = ['lab_name']
#
#     # Basic redirect
#     def get_success_prompt(self):
#         return reverse('lab:thanks')



def addQuestionsToLab(request):
    # Create the formset, specifying the form and formset we want to use.
    TestQuestionFormSet = formset_factory(testQuestionForm, formset=BaseTestQuestionFormSet)

    if request.method == 'POST':
        question_formset = TestQuestionFormSet(request.POST)
        test_lab_form = testLabForm(request.POST)

        if test_lab_form.is_valid() and question_formset.is_valid():

            test_lab = testLab(lab_name=test_lab_form.cleaned_data.get('lab_name'))
            test_lab.save()
            # Now save the data for each form in the formset
            lab_questions = []

            for question_form in question_formset:
                name = question_form.cleaned_data.get('name')
                prompt = question_form.cleaned_data.get('prompt')

                if name and prompt:
                    tempQuestion = testQuestion(test_lab=test_lab, question_name=name, question_prompt=prompt)
                    tempQuestion.save()
        return render_to_response('lab/index.html')




    else:
        question_formset = TestQuestionFormSet()
        test_lab_form = testLabForm()
        context = { 'question_formset': question_formset, 'lab_form': test_lab_form}
        # context = { 'lab_form': lab_form,}
        # context['lab_form'] = lab_form

    return render(request, 'lab/createbiglab2.html', context)
