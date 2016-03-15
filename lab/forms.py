from django import forms
from django.db import models
from lab.models import Lab, Variable, Submission, RawData, Question
from django.utils import timezone
from django.forms.formsets import BaseFormSet

class SubmissionForm(forms.Form):
    w_number = forms.CharField(max_length=20)

# class RawDataForm(forms.ModelForm):
#     class Meta:
#         model = RawData
#         fields = ['raw_data']
#         widgets = {
#             'raw_data': forms.NumberInput(attrs={'style': 'width:80px', 'step' : 0.0001}),
#         }


class RawDataForm(forms.ModelForm):
    class Meta:
        model = RawData
        fields = ['raw_data']
        widgets = {
            'raw_data': forms.NumberInput(attrs={'style': 'width:80px', 'step' : 0.0001}),
        }


class QuestionForm(forms.Form):
    fields = {}
    def __init__(self, question, request, questionNum, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        variables = Variable.objects.filter(question=question)
        self.question = question
        self.fields['variable_forms'] = []
        self.fields['num_of_trials'] = question.trials
        self.fields['prompt'] = question.prompt
        i = 0
        for variable in variables:
            variableNum = i
            self.fields['variable_forms'].append(VariableForm(question.trials, variable, variableNum, questionNum, request))
            i = i + 1

class VariableForm(forms.Form):
    fields = {}
    def __init__(self, trials, variable, variableNum, questionNum, request, *args, **kwargs):
        super(VariableForm, self).__init__(*args, **kwargs)
        self.variable = variable
        self.fields['raw_data_forms'] = []
        self.fields['name'] = variable.variable_name
        for i in range(0, trials):
            raw_name = "%d-%d-%d" % (questionNum, variableNum, i)
            if request.method == "GET":
                print "Using none?!?!?!"
                self.fields['raw_data_forms'].append(RawDataForm(prefix = raw_name))
            else:
                print "Filling in the raw DATA!"
                self.fields['raw_data_forms'].append(RawDataForm(request.POST, prefix = raw_name))
