from django.contrib import admin
import nested_admin
from lab.models import Lab, Question, Variable, Submission, RawData


class VariableInLine(nested_admin.NestedTabularInline):
    model = Variable
    extra = 0

class QuestionInLine(nested_admin.NestedStackedInline):
    model = Question
    inlines = [VariableInLine]
    extra = 0

class LabAdmin(nested_admin.NestedModelAdmin):
    fieldsets = [
        ('Lab information', {'fields': ['lab_name']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [QuestionInLine]
    list_display = ('lab_name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['lab_name']

class RawDataInLine(nested_admin.NestedStackedInline):
    model = RawData
    extra = 0


class SubmissionAdmin(nested_admin.NestedModelAdmin):
    fieldsets = [
        ('W Number', {'fields': ['w_number']}),
    ]
    inlines = [RawDataInLine]
    list_display = ('w_number',)
    search_fields = ['w_number']

admin.site.register(Lab, LabAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(RawData)
