from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *

# Authentication Views
class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == User.TEACHER

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == User.ADMIN

# User Management Views
class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'lms_app/registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, 'Account created successfully!')
        return super().form_valid(form)

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'lms_app/profile.html', {'form': form})

# Course Management Views
class CourseListView(ListView):
    model = Course
    template_name = 'lms_app/course_list.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.role == User.TEACHER:
            return Course.objects.filter(teacher=self.request.user)
        return Course.objects.all()

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'lms_app/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = self.object.module_set.all().order_by('order')
        if self.request.user.role == User.STUDENT:
            context['enrolled'] = Enrollment.objects.filter(
                student=self.request.user,
                course=self.object
            ).exists()
        return context

class CourseCreateView(TeacherRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'lms_app/course_form.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)

# Module and Content Management Views
class ModuleCreateView(TeacherRequiredMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = 'lms_app/module_form.html'

    def form_valid(self, form):
        course = get_object_or_404(Course, pk=self.kwargs['course_pk'])
        form.instance.course = course
        return super().form_valid(form)

class LectureMaterialCreateView(TeacherRequiredMixin, CreateView):
    model = LectureMaterial
    form_class = LectureMaterialForm
    template_name = 'lms_app/material_form.html'

    def form_valid(self, form):
        module = get_object_or_404(Module, pk=self.kwargs['module_pk'])
        form.instance.module = module
        return super().form_valid(form)

# Assignment Management Views
class AssignmentCreateView(TeacherRequiredMixin, CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'lms_app/assignment_form.html'

    def form_valid(self, form):
        form.instance.course_id = self.kwargs['course_pk']
        return super().form_valid(form)

@login_required
def submit_assignment(request, assignment_pk):
    assignment = get_object_or_404(Assignment, pk=assignment_pk)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.assignment = assignment
            submission.save()
            messages.success(request, 'Assignment submitted successfully!')
            return redirect('course_detail', pk=assignment.course.pk)
    else:
        form = SubmissionForm()
    return render(request, 'lms_app/submission_form.html', {
        'form': form,
        'assignment': assignment
    })

# Grading Views
@login_required
def grade_submission(request, submission_pk):
    submission = get_object_or_404(Submission, pk=submission_pk)
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.submission = submission
            grade.graded_by = request.user
            grade.save()
            messages.success(request, 'Grade submitted successfully!')
            return redirect('submission_list')
    else:
        form = GradeForm()
    return render(request, 'lms_app/grade_form.html', {
        'form': form,
        'submission': submission
    })

# Enrollment Views
@login_required
def enroll_course(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if request.user.role != User.STUDENT:
        messages.error(request, 'Only students can enroll in courses.')
        return redirect('course_detail', pk=course_pk)
    
    Enrollment.objects.get_or_create(student=request.user, course=course)
    messages.success(request, f'Successfully enrolled in {course.title}')
    return redirect('course_detail', pk=course_pk)
