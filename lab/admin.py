from django.contrib import admin
from lab.models import Lab, Submission, testLab, testQuestion
# Register your models here.

admin.site.register(Lab)
admin.site.register(Submission)



class ChoiceInline(admin.TabularInline):
    model = testQuestion
    extra = 1
    
class LabAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Lab information', {'fields': ['lab_name']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('lab_name',)
    search_fields = ['lab_name']


admin.site.register(testLab, LabAdmin)
admin.site.register(testQuestion)
