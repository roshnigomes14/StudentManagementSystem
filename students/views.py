from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator


# Home Page
def home(request):
    return render(request, 'students/home.html')


# Dashboard
# Dashboard
def dashboard(request):
    total_students = Student.objects.count()
    total_departments = Student.objects.values('department').distinct().count()
    ise_students = Student.objects.filter(department__iexact='ISE').count()

    context = {
        'total_students': total_students,
        'total_departments': total_departments,
        'ise_students': ise_students,
    }

    return render(request, 'students/dashboard.html', context)

   
def login_user(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'students/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


# Display and Search Students
def student_list(request):
    query = request.GET.get('q')

    if query:
        students = Student.objects.filter(name__icontains=query)
    else:
        students = Student.objects.all()

    paginator = Paginator(students, 5)   # 5 students per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'students/student_list.html', {
        'page_obj': page_obj,
        'query': query,
    })


# Add Student
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully!")
            return redirect('student_list')
    else:
        form = StudentForm()

    return render(request, 'students/student_form.html', {
        'form': form
    })


# Edit Student
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)

        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect('student_list')

    else:
        form = StudentForm(instance=student)

    return render(request, 'students/student_form.html', {
        'form': form
    })

# Delete Student
# Delete Student
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully!")
        return redirect('student_list')

    return render(request, 'students/student_delete.html', {
        'student': student
    })


# Student Detail Page
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)

    return render(request, 'students/student_detail.html', {
        'student': student
    })