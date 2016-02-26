from django import forms
from lab.models import Lab, Submission, BigLab, Question, testQuestion
from django.utils import timezone
from django.forms.formsets import BaseFormSet


class BigLabForm(forms.ModelForm):
    class Meta:
        model = BigLab
        exclude = ('pub_date',)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('bigLab',)


class BigLabForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['lab_name'] = forms.CharField(max_length=30, widget=forms.TextInput(attrs={ 'placeholder': 'Lab Name', }))


class testQuestionForm(forms.Form):
    name = forms.CharField( max_length=100, widget=forms.TextInput(attrs={ 'placeholder': 'Question Name', }), required=False)
    prompt = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'Question Prompt', }), required=False)

class testLabForm(forms.Form):
    lab_name = forms.CharField( max_length=100, widget=forms.TextInput(attrs={ 'placeholder': 'Lab Name', }), required=False)
    

class BaseTestQuestionFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        names = []
        prompts = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                name = form.cleaned_data['name']
                prompt = form.cleaned_data['prompt']
                # Check that no two links have the same anchor or URL
                if name and prompt:
                    if name in names:
                        duplicates = True
                    names.append(name)

                    if prompt in prompts:
                        duplicates = True
                    prompts.append(prompt)

                if duplicates:
                    raise forms.ValidationError(
                        'Question must have unique names and prompts',
                        code='duplicate_links'
                    )

                # Check that all links have both an anchor and URL
                if name and not prompt:
                    raise forms.ValidationError(
                        'All questions must have a prompt.',
                        code='missing_prompt'
                    )
                elif prompt and not name:
                    raise forms.ValidationError(
                        'All questions must have a name.',
                        code='missing_name'
                    )

# ----------------------------------------------------------------------------
# Old Stuff
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
