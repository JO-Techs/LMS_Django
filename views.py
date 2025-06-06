from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.utils.http import urlencode

from .forms import *
from .models import *


# Home View
class HomeView(TemplateView):
    template_name = 'lms_app/home.html'

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
    template_name = 'lms_app/authentication/register.html'
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
    return render(request, 'lms_app/authentication/profile.html', {'form': form})

# Course Management Views
class CourseListView(ListView):
    model = Course
    template_name = 'lms_app/courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == User.TEACHER:
            return Course.objects.filter(teacher=self.request.user).order_by('title')
        return Course.objects.all().order_by('title')

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'lms_app/courses/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = self.object.module_set.all().order_by('order')
        return context

class CourseCreateView(TeacherRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'lms_app/courses/course_form.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)

# Module and Content Management Views
class ModuleCreateView(TeacherRequiredMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = 'lms_app/modules/module_form.html'

    def form_valid(self, form):
        course = get_object_or_404(Course, pk=self.kwargs['course_pk'])
        form.instance.course = course
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('course_detail', kwargs={'pk': self.kwargs['course_pk']})

class ModuleDetailView(LoginRequiredMixin, DetailView):
    model = Module
    template_name = 'lms_app/modules/module_detail.html'
    context_object_name = 'module'

class LectureMaterialCreateView(TeacherRequiredMixin, CreateView):
    model = LectureMaterial
    form_class = LectureMaterialForm
    template_name = 'lms_app/modules/material_form.html'

    def form_valid(self, form):
        module = get_object_or_404(Module, pk=self.kwargs['module_pk'])
        form.instance.module = module
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('module_detail', kwargs={'pk': self.kwargs['module_pk']})

# Assignment Management Views
class AssignmentCreateView(TeacherRequiredMixin, CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'lms_app/assignments/assignment_form.html'

    def form_valid(self, form):
        form.instance.course_id = self.kwargs['course_pk']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('course_detail', kwargs={'pk': self.kwargs['course_pk']})

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
    return render(request, 'lms_app/assignments/submission_form.html', {
        'form': form,
        'assignment': assignment
    })

# Grading Views
class SubmissionListView(TeacherRequiredMixin, ListView):
    model = Submission
    template_name = 'lms_app/submissions/submission_list.html'
    context_object_name = 'submissions'
    paginate_by = 20

    def get_queryset(self):
        # Teachers can only see submissions for their courses
        teacher_courses = Course.objects.filter(teacher=self.request.user)
        return Submission.objects.filter(assignment__course__in=teacher_courses).order_by('-submitted_on')

@login_required
def grade_submission(request, submission_pk):
    submission = get_object_or_404(Submission, pk=submission_pk)
    # Ensure only the teacher of the course can grade
    if request.user != submission.assignment.course.teacher:
        messages.error(request, "You don't have permission to grade this submission.")
        return redirect('course_list')
        
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

# Quiz Management Views
class QuizCreateView(TeacherRequiredMixin, CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'lms_app/quizzes/quiz_form.html'
    success_url = reverse_lazy('quiz_list')

    def get_initial(self):
        initial = super().get_initial()
        course_id = self.request.GET.get('course')
        if course_id:
            initial['course'] = course_id
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        course_id = self.request.GET.get('course')
        if course_id:
            form.fields['course'].queryset = Course.objects.filter(pk=course_id)
        else:
            # Only show courses taught by this teacher
            form.fields['course'].queryset = Course.objects.filter(teacher=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        return redirect('add_questions', quiz_pk=self.object.pk)

def add_questions(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('add_questions', quiz_pk=quiz_pk)
    else:
        form = QuestionForm()
    questions = quiz.questions.all()
    return render(request, 'lms_app/quizzes/question_form.html', {'form': form, 'quiz': quiz, 'questions': questions})

class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = 'lms_app/quizzes/quiz_list.html'
    context_object_name = 'quizzes'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.role == User.TEACHER:
            return Quiz.objects.filter(created_by=self.request.user)
        return Quiz.objects.all()