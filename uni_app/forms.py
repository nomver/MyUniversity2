from django import forms
from uni_app import models

class AddUniversityForm(forms.ModelForm):
    class Meta:
        model=models.University
        fields=['name','address']

class AddDepartmentForm(forms.ModelForm):
    class Meta:
        model=models.Department
        fields=['name']

class AddProgramForm(forms.ModelForm):
    class Meta:
        model=models.Program
        fields=['name','semester']

class AddSubjectForm(forms.ModelForm):
    class Meta:
        model=models.Subject
        fields=['title','image','program']

        widgets={
            'image':forms.FileInput(attrs={'required':'required','accept':"image/*"}),
            }

class AddLectureForm(forms.ModelForm):
    class Meta:
        model=models.Lecture
        fields=['title','audio','related_files']

class AddAssignmentForm(forms.ModelForm):
    class Meta:
        model=models.Assignment
        fields=['assignment','due_on']

        widgets={
            'due_on':forms.DateTimeInput(attrs={'type':'date'})
        }

class SubmittedAssignmentForm(forms.ModelForm):
    class Meta:
        model=models.SubmittedAssignment
        fields=['submitted_docs',]

        
        widgets={
            'submitted_docs':forms.FileInput(attrs={'required':'required'}),
            }