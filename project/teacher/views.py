from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Teacher
from .forms import AddStudentForm, CourseForm
from .forms import TeacherProfileForm
from courses.models import UserCourse,Course
from courses.forms.course_material_form import CourseMaterialForm
from django.contrib.auth.models import User
#from user_profile.models import CustomUser
from courses.models.user_course import CourseMaterial
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
#from .decorators import teacher_required

@login_required
def teacher_dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    return render(request, 'teacher/dashboard.html', {'teacher': teacher})

@login_required
def edit_teacher_profile(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = TeacherProfileForm(instance=teacher)
    return render(request, 'teacher/edit_profile.html', {'form': form})

@login_required
def manage_courses(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = teacher.courses.all()
    return render(request, 'teacher/manage_courses.html', {'courses': courses})

def teacher_courses(request):
    teacher = Teacher.objects.get(user=request.user)
    
    courses = teacher.courses.all()

    return render(request, 'teacher/teacher_courses.html', {'courses': courses})

# def create_course(request):
#     if request.method == 'POST':
#         form = CourseForm(request.POST)
#         if form.is_valid():
#             course = form.save(commit=False)
#             teacher = request.user.teacher
#             course.save()
#             teacher.courses.add(course)
#             return redirect('teacher_courses')
#     else:
#         form = CourseForm()

#     return render(request, 'teacher/create_course.html', {'form': form})

def course_students_stats(request, course_id):
    course = Course.objects.get(id=course_id) 
    students = UserCourse.objects.filter(course=course) 
    stats = [{'student': student.user.username, 'grade': student.grade, 'completion_date': student.date} for student in students]

    return render(request, 'teacher/course_stats.html', {'course': course, 'stats': stats})

def add_student_to_course(request):
    teacher = Teacher.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = AddStudentForm(teacher, request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            course = form.cleaned_data['course']
            
            
            UserCourse.objects.create(user=student, course=course)
            return redirect('teacher_courses') 
    else:
        form = AddStudentForm(teacher)

    return render(request, 'teacher/add_student_to_course.html', {'form': form})

@login_required
def remove_student_from_course(request, student_id, course_id):
    teacher = Teacher.objects.get(user=request.user)
    course = get_object_or_404(Course, id=course_id)
    student = get_object_or_404(User, id=student_id)
    
    if student in course.users.all():
        UserCourse.objects.filter(user=student, course=course).delete()
    
    return redirect('teacher_courses')

@login_required
def upload_course_material(request, course_id):
    teacher = Teacher.objects.get(user=request.user) 
    course = Course.objects.get(id=course_id)  

    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course 
            material.save()
            return redirect('course_details', course_id=course.id)  
    else:
        form = CourseMaterialForm()

    return render(request, 'teacher/upload_course_material.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        
        user = form.get_user()

        
        if hasattr(user, 'teacher_profile'):
            return redirect('teacher_dashboard') 

        return super().form_valid(form)

@login_required  
#@teacher_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user  
            course.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'teacher/create_course.html', {'form': form})