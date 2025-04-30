from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os

class User(AbstractUser):
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (ADMIN, 'Admin'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                              limit_choices_to={'role': User.TEACHER})
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              limit_choices_to={'role': User.STUDENT})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'course']

class Module(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']

def lecture_material_path(instance, filename):
    return f'course_{instance.module.course.id}/module_{instance.module.id}/{filename}'

class LectureMaterial(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to=lecture_material_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        # Validate file type
        ext = os.path.splitext(self.file.name)[1]
        valid_extensions = ['.pdf', '.mp4', '.pptx', '.doc', '.docx']
        if ext.lower() not in valid_extensions:
            raise ValidationError('Unsupported file type.')

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    max_points = models.DecimalField(max_digits=5, decimal_places=2)

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    submitted_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['assignment', 'student']

class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE)
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField()
    graded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 limit_choices_to={'role': User.TEACHER})
    graded_at = models.DateTimeField(auto_now_add=True)
