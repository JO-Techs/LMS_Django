from django import forms
from .models import User, Course, Module, LectureMaterial, Assignment, Submission, Grade

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'order']

class LectureMaterialForm(forms.ModelForm):
    class Meta:
        model = LectureMaterial
        fields = ['title', 'description', 'file']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'content', 'due_date', 'max_points']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['marks', 'feedback']
