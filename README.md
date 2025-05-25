# LMS Project

A Learning Management System built with Django.

## Features

- User authentication with role-based access control (Student, Teacher, Admin)
- Course management
- Module and learning materials organization
- Assignment submission and grading
- RESTful API for integration with other systems

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/LMS_Project.git
cd LMS_Project
```

2. Create and activate a virtual environment:
```
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Apply migrations:
```
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```
python manage.py createsuperuser
```

6. Run the development server:
```
python manage.py runserver
```

7. Access the application at http://127.0.0.1:8000/

## Usage

### User Roles

- **Students**: Can browse courses, enroll in courses, access learning materials, and submit assignments
- **Teachers**: Can create courses, add modules and materials, create assignments, and grade submissions
- **Admins**: Have full access to all features and can manage users

### Course Management

Teachers can create courses, organize them into modules, and add various types of learning materials.

### Assignment Workflow

1. Teachers create assignments with due dates
2. Students submit their work before the deadline
3. Teachers grade submissions and provide feedback

## License

This project is licensed under the MIT License - see the LICENSE file for details.