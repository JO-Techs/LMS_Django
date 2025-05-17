from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, Module, LectureMaterial, Assignment, Submission, Grade, Enrollment

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'profile_picture', 'bio')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description', 'teacher__username')
    inlines = [ModuleInline]

class LectureMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('title', 'description')

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'max_points')
    list_filter = ('due_date', 'course')
    search_fields = ('title', 'content')

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'submitted_on')
    list_filter = ('submitted_on', 'assignment')
    search_fields = ('student__username', 'assignment__title')

class GradeAdmin(admin.ModelAdmin):
    list_display = ('submission', 'marks', 'graded_by', 'graded_at')
    list_filter = ('graded_at',)
    search_fields = ('submission__student__username', 'submission__assignment__title')

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_on')
    list_filter = ('enrolled_on', 'course')
    search_fields = ('student__username', 'course__title')

# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Module)
admin.site.register(LectureMaterial, LectureMaterialAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)