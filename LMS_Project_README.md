
# LMS (Learning Management System) - Project

## Overview

This is a **Learning Management System (LMS)** built using **Django**, **Django REST Framework (DRF)**, **PostgreSQL**, **Redis**, and **Celery**. It allows users to register, browse, and enroll in courses. Teachers can create courses, lessons, assignments, and grade submissions. Students can track their progress and receive notifications.

## Features

- **User Authentication & Roles**: User registration with roles (Student, Teacher, Admin), JWT authentication.
- **Course Management**: Teachers can create and manage courses and lessons, students can view and enroll in courses.
- **Assignments & Grading**: Teachers can create assignments, students can submit them, and Celery handles background grading.
- **Progress Tracking**: Students can track their progress in each course.
- **Notifications**: Email or SMS notifications for course updates, new assignments, etc.
- **Caching**: Redis is used to cache frequently accessed data like course lists and student progress.
- **Admin Panel**: Admins can manage users, courses, and assignments via the Django Admin interface.

## Technologies & Tools

- **Django**: Web framework for building the application.
- **Django REST Framework (DRF)**: For creating APIs.
- **PostgreSQL**: Relational database for storing user data, courses, and assignments.
- **Redis**: Caching frequently accessed data and used by Celery for background tasks.
- **Celery**: For asynchronous tasks like grading and notifications.
- **JWT Authentication**: For secure user authentication.
- **Docker** (Optional): For containerizing the application.

## Project Structure

```
lms_project/
│
├── lms_app/                     # Main Django app for LMS functionality
│   ├── migrations/              # Database migrations
│   ├── models/                  # Django models (User, Course, Lesson, Assignment, etc.)
│   ├── views/                   # Views for API endpoints (DRF ViewSets, Generic Views)
│   ├── serializers/             # DRF serializers
│   ├── urls/                    # App-specific URL routing
│   └── tasks/                   # Celery tasks for background jobs
│
├── lms_project/                 # Project settings
│   ├── __init__.py
│   ├── settings.py              # Django settings (including Celery & Redis)
│   ├── urls.py                  # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── requirements.txt            # Project dependencies
├── Dockerfile                  # Docker configuration (optional)
└── manage.py                   # Django management script
```

## Models

### User Model
- `username`, `email`, `password`, `role` (Student, Teacher, Admin)

### Course Model
- `title`, `description`, `teacher` (ForeignKey to User), `created_at`, `updated_at`

### Lesson Model
- `title`, `content`, `course` (ForeignKey to Course), `order`

### Assignment Model
- `title`, `course` (ForeignKey to Course), `deadline`, `created_at`

### Submission Model
- `student` (ForeignKey to User), `assignment` (ForeignKey to Assignment), `submitted_at`, `grade`

### Progress Model
- `student` (ForeignKey to User), `course` (ForeignKey to Course), `progress` (float: 0-100%)

## API Endpoints

### User Authentication
- **POST** `/auth/register/` - Register a new user.
- **POST** `/auth/login/` - Log in and get JWT token.
- **POST** `/auth/logout/` - Log out the user.

### Course Management
- **GET** `/courses/` - List all courses.
- **POST** `/courses/` - Create a new course (Teacher only).
- **GET** `/courses/{course_id}/` - Get details of a course.
- **POST** `/courses/{course_id}/enroll/` - Enroll in a course.

### Lesson Management
- **GET** `/courses/{course_id}/lessons/` - List all lessons in a course.
- **POST** `/courses/{course_id}/lessons/` - Create a new lesson (Teacher only).

### Assignment Management
- **GET** `/courses/{course_id}/assignments/` - List all assignments for a course.
- **POST** `/courses/{course_id}/assignments/` - Create a new assignment (Teacher only).
- **POST** `/assignments/{assignment_id}/submit/` - Submit an assignment (Student only).

### Progress Tracking
- **GET** `/courses/{course_id}/progress/` - Get progress for a student in a course.

## Celery for Background Tasks

Celery is used for tasks like:
- Grading assignments asynchronously.
- Sending email/SMS notifications.

### Setup Celery
1. Install Redis locally or use a cloud Redis service.
2. Update Django settings to use Celery and Redis as the broker.

## Redis for Caching

Redis is used to cache frequently accessed data, such as:
- Course lists.
- Student progress.

### Set Up Redis
1. Install Redis locally or use a cloud Redis service.
2. Configure Redis in `settings.py`.

## Requirements

Install the project dependencies:
```
pip install -r requirements.txt
```

### Docker Setup (Optional)

If you choose to containerize the project using Docker, here’s a simple Dockerfile:

```
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Running the Project

1. Set up PostgreSQL and Redis.
2. Run database migrations:
   ```
   python manage.py migrate
   ```
3. Start the development server:
   ```
   python manage.py runserver
   ```

### Additional Notes

- Use **Django Admin** to manage courses, users, and assignments.
- **Celery** and **Redis** need to be running for background tasks.
- To scale the app, consider deploying with **Docker**, **Heroku**, or **AWS**.
