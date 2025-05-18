from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home page
    path('', views.HomeView.as_view(), name='home'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='lms_app/authentication/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('profile/', views.profile_view, name='profile'),

    # Course URLs
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('course/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('course/<int:course_pk>/enroll/', views.enroll_course, name='enroll_course'),

    # Module URLs
    path('course/<int:course_pk>/module/create/', 
         views.ModuleCreateView.as_view(), name='module_create'),
    path('module/<int:pk>/', 
         views.ModuleDetailView.as_view(), name='module_detail'),

    # Material URLs
    path('module/<int:module_pk>/material/create/',
         views.LectureMaterialCreateView.as_view(), name='material_create'),

    # Assignment URLs
    path('course/<int:course_pk>/assignment/create/',
         views.AssignmentCreateView.as_view(), name='assignment_create'),
    path('assignment/<int:assignment_pk>/submit/',
         views.submit_assignment, name='submit_assignment'),

    # Grading URLs
    path('submission/<int:submission_pk>/grade/',
         views.grade_submission, name='grade_submission'),
    path('submissions/', views.SubmissionListView.as_view(), name='submission_list'),
]