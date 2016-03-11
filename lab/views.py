from django.shortcuts import get_object_or_404, render, render_to_response
from django.views import generic
from django.template import RequestContext
from lab.models import Lab, Question, Variable, Submission, RawData
from lab.forms import SubmissionForm, RawDataForm, VariableForm, QuestionForm
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django import forms
from django.db import models
from django.forms import formset_factory


# Fine tuned BootStrap - 4 Pages, Home, Submissions, Creations, Results

class Home(generic.TemplateView):
    template_name = 'lab/home.html'

class Submissions(generic.TemplateView):
    template_name = 'lab/submissions.html'

class SubmissionsIndex(generic.ListView):
    model = Lab
    template_name = 'lab/submissions.html'
    context_object_name = 'lab_list'

    # All the labs that it will be listing
    def get_queryset(self):
        return Lab.objects.all()

def CreateSubmission(request, **kwargs):
    context = RequestContext(request)
    lab = get_object_or_404(Lab, pk=kwargs['pk'])
    questions = Question.objects.filter(lab=lab)
    submission_form = SubmissionForm(request.POST or None)
    question_forms = []


    for question in questions:
        tempForm = QuestionForm(question, request.POST or None)
        question_forms.append(tempForm)


    if request.method == "POST":



        for question_form in question_forms:
            for variable_form in question_form.fields['variable_forms']:
                print variable_form.variable.variable_name
                for raw_data_form in variable_form.fields['raw_data_forms']:
                    print str(raw_data_form.fields['raw_data'])



        return render_to_response('lab/home.html', context)

    # ---------------------------------------------------
    else:
        context['lab'] = lab
        context['questions'] = questions
        context['submission_form'] = submission_form
        context['question_forms'] = question_forms


    return render_to_response('lab/createsubmission.html', context)


# Links to the page that allows users to submit lab submissions
# class CreateSubmission(generic.CreateView):
#     template_name = 'lab/createsubmission.html'
#     model = Submission
#     fields = ['w_number']
#
#     # Used to get the lab object into the page, so we can display questions from it
#     def get_context_data(self, **kwargs):
#         context = {}
#         context['lab'] = get_object_or_404(Lab, pk=self.kwargs['pk'])
#         return super(generic.CreateView, self).get_context_data(**context)
#
#     # Ensures all the forms fields are valid. Also links up the foreign key to the parent lab
#     def form_valid(self, form):
#         form.instance.lab = get_object_or_404(Lab, pk=self.kwargs['pk'])
#         return super(CreateSubmission, self).form_valid(form)
#
#     # Basic redirect
#     def get_success_prompt(self):
#         return reverse('lab:thanks')
# Static HTML pages used for user movement
class Thanks(generic.TemplateView):
    template_name = 'lab/thanks.html'

class Index(generic.TemplateView):
    template_name = 'lab/index.html'


class BootStrap(generic.TemplateView):
    template_name = 'lab/bootstrap_example.html'
# ---------------------------------------
#
# # Displays lab options, directs to a submission for that lab
# class LabIndex(generic.ListView):
#     template_name = 'lab/labindex.html'
#     context_object_name = 'lab_list'
#
#     # All the labs that it will be listing
#     def get_queryset(self):
#         return Lab.objects.all()
#
# # Same as LabIndex, but directs them to the already made submissions
# class SubmissionIndex(generic.ListView):
#     model = Lab
#     template_name = 'lab/submissionindex.html'
#     context_object_name = 'lab_list'
#
#     # All the labs that it will be listing
#     def get_queryset(self):
#         return Lab.objects.all()
#
# # Links to the page that allows users to create labs
# class CreateLab(generic.CreateView):
#     template_name = 'lab/createlab.html'
#     model = Lab
#     fields = ['lab_name', 'lab_question']
#
#     # Basic redirect
#     def get_success_prompt(self):
#         return reverse('lab:thanks')
#
# # Links to the page that allows users to submit lab submissions
# class CreateSubmission(generic.CreateView):
#     template_name = 'lab/createsubmission.html'
#     model = Submission
#     fields = ['student_name', 'student_email', 'input_int']
#
#     # Used to get the lab object into the page, so we can display questions from it
#     def get_context_data(self, **kwargs):
#         context = {}
#         context['lab'] = get_object_or_404(Lab, pk=self.kwargs['pk'])
#         return super(generic.CreateView, self).get_context_data(**context)
#
#     # Ensures all the forms fields are valid. Also links up the foreign key to the parent lab
#     def form_valid(self, form):
#         form.instance.lab = get_object_or_404(Lab, pk=self.kwargs['pk'])
#         return super(CreateSubmission, self).form_valid(form)
#
#     # Basic redirect
#     def get_success_prompt(self):
#         return reverse('lab:thanks')
#
# # Displays all the submissions of one lab
# class SubmissionView(generic.ListView):
#     template_name = 'lab/submissionview.html'
#     context_object_name = 'submission_list'
#
#     # Gets all of the submissions to display
#     def get_queryset(self, **kwargs):
#         lab = get_object_or_404(Lab, pk=self.kwargs['pk'])
#         return lab.submission_set.all()
#
#     # Loads in the lab to the context, used to print lab info
#     def get_context_data(self, **kwargs):
#         context = {}
#         lab = get_object_or_404(Lab, pk=self.kwargs['pk'])
#         context['lab'] = lab
#         return super(generic.ListView, self).get_context_data(**context)
#
# # Works up to this point
# # ----------------------------------------------------------------------------
# # Anything under here is being tested
#
# # Creates a basic BigLab, need to work on this
# # class CreateBigLab(generic.CreateView):
# #     template_name = 'lab/createbiglab.html'
# #     model = BigLab
# #     fields = ['lab_name']
# #
# #     # Basic redirect
# #     def get_success_prompt(self):
# #         return reverse('lab:thanks')
#
# # def CreateBigLab(request):
# #     template_name = 'lab/createbiglab.html'
# #     model = BigLab
# #     fields = ['lab_name']
# #
# #     # Basic redirect
# #     def get_success_prompt(self):
# #         return reverse('lab:thanks')
#
#
#
# def addQuestionsToLab(request):
#     # Create the formset, specifying the form and formset we want to use.
#     TestQuestionFormSet = formset_factory(testQuestionForm, formset=BaseTestQuestionFormSet)
#
#     if request.method == 'POST':
#         question_formset = TestQuestionFormSet(request.POST)
#         test_lab_form = testLabForm(request.POST)
#
#         if test_lab_form.is_valid() and question_formset.is_valid():
#
#             test_lab = testLab(lab_name=test_lab_form.cleaned_data.get('lab_name'))
#             test_lab.save()
#             # Now save the data for each form in the formset
#             lab_questions = []
#
#             for question_form in question_formset:
#                 name = question_form.cleaned_data.get('name')
#                 prompt = question_form.cleaned_data.get('prompt')
#
#                 if name and prompt:
#                     tempQuestion = testQuestion(test_lab=test_lab, question_name=name, question_prompt=prompt)
#                     tempQuestion.save()
#         return render_to_response('lab/index.html')
#
#
#
#
#     else:
#         question_formset = TestQuestionFormSet()
#         test_lab_form = testLabForm()
#         context = { 'question_formset': question_formset, 'lab_form': test_lab_form}
#         # context = { 'lab_form': lab_form,}
#         # context['lab_form'] = lab_form
#
#     return render(request, 'lab/createbiglab2.html', context)
