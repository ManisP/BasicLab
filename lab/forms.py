from django import forms
from lab.models import Lab, Submission
from django.utils import timezone


class BasicLabForm(forms.Form):
	input_int = forms.IntegerField(label = 'Answer:')
	student_name = forms.CharField(label = 'Student Name:')
	student_email = forms.CharField(label = 'Student Email:')

class CreateALab(forms.Form):
	lab_name = forms.CharField(label = 'Lab Name')
	lab_question = forms.CharField(label = 'Lab Question')

	def createLab(self):
		tempLab = Lab(lab_name = self.cleaned_data['lab_name'], lab_question = self.cleaned_data['lab_question'],  pub_date = timezone.now())
		tempLab.save()
		return tempLab

class CreateASubmission(forms.Form):
    student_name = forms.CharField(label = 'Student Name')
    student_email = forms.EmailField( label = 'Student Email')
    input_int = forms.IntegerField()

    def createSubmission(self):
	    tempSubmission = Submission(student_name = self.cleaned_data['student_name'], student_email = self.cleaned_data['student_email'],  input_int = self.cleaned_data['input_int'])
	    tempSubmission.save()
	    return tempSubmission
