from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from .models import *
from .forms import *

def admin_home(request):
    total_teacher = Staff.objects.all().count()
    total_students = Student.objects.all().count()
    total_subjects = Clazz.objects.all()

    context = {
        'total_students': total_students,
        'total_teacher': total_teacher,
        'total_subject': total_subjects,
    }

    return render(request, 'admin_template/admin_home.html', context)


# Manage staff section
def manage_staff(request):

    staff_id = request.GET.get('staff_id')

    if staff_id:
        all_staff = Clazz.objects.filter(staff_id=staff_id)
    else:
        all_staff = Clazz.objects.all()

    context = {
        'all_staff': all_staff
    }

    return render(request, "admin_template/manage_staff.html", context)



def add_staff(request):
    form = StaffForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': 'Add Staff'}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            staff_id = form.cleaned_data.get('staff_id')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')

            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2, first_name=first_name, last_name=last_name
                )

                user.gender = gender
                user.staff.staff_id = staff_id
                user.save()
                messages.success(request, 'Successfully Added')
                return redirect(reverse('main_app:add_staff'))
            
            except Exception as e:
                messages.error(request, 'Could not add ' + str(e))
        else:
            messages.error(request, 'Please fulfil all requirements')
    
    return render(request, 'admin_template/add_staff.html', context)

def staff_detail(request):
    pass

def delete_staff(request):
    pass

# Manage student section
def manage_student(request):
    search_query = request.GET.get('search_query', '')
    
    students = Student.objects.filter(student_id__icontains=search_query)
    context = {'students': students, 'search_query': search_query}
    return render(request, 'admin_template/manage_student.html', context)

def add_student(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    image_form = StudentImageForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'image_form': image_form, 'page_title': 'Add Student'}
    
    if request.method == 'POST':
        if form.is_valid() and image_form.is_valid():
            # Retrieve form data for student creation
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            student_id = form.cleaned_data.get('student_id')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            session = form.cleaned_data.get('session')
            
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3, first_name=first_name, last_name=last_name
                )

                # Create student instance
                user.gender = gender
                user.student.student_id = student_id
                user.student.session = session
                user.save()

                # Associate image with the student
                image_instance = image_form.save(commit=False)
                image_instance.student = user.student
                image_instance.save()

                messages.success(request, 'Successfully Added')
                return redirect(reverse('main_app:add_student'))
            
            except Exception as e:
                messages.error(request, 'Could not add ' + str(e))
        else:
            messages.error(request, 'Please fulfill all requirements')

    return render(request, 'admin_template/add_student.html', context)

def delete_student(request, student_id):
    try:
        student = Student.objects.get(student_id=student_id)
        student.admin.delete()  # Delete the associated user instance
        messages.success(request, 'Student deleted successfully')
    except Student.DoesNotExist:
        messages.error(request, 'Student not found')
    
    return redirect('main_app:manage_student')

# Manage class section

def manage_clazz(request):

    semesters = Clazz.objects.values_list('semester', flat=True).distinct()

    # Filter classes by semester if provided
    semester = request.GET.get('semester')

    if semester:
        all_clazz = Clazz.objects.filter(semester=semester)
    else:
        all_clazz = Clazz.objects.all()


    context = {
        'semesters': semesters,
        'all_clazz': all_clazz,
    }

    return render(request, "admin_template/manage_class.html", context)

def add_class(request):
    form = ClazzForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Subject'
    }

    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            class_id = form.cleaned_data.get('clazz_id')
            semester = form.cleaned_data.get('semester')
            teacher = form.cleaned_data.get('teacher')
            try:
                clazz = Clazz()
                clazz.name = name
                clazz.clazz_id = class_id
                clazz.teacher = teacher
                clazz.semester = semester
                clazz.save()
                messages.success(request, 'Successfully Added')
                return redirect(reverse('main_app:add_class'))
            
            except Exception as e:
                messages.error(request, "Could not add " + str(e))

        else:
            messages.error(request, "Fill Form Properly")

    return render(request, 'admin_template/add_class.html', context)


def class_detail(request, clazz_id):
    clazz = get_object_or_404(Clazz, pk=clazz_id)
    students = clazz.students.all()

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        try:
            student = Student.objects.get(student_id=student_id)
            clazz.students.add(student)
            return redirect('main_app:admin_class_detail', clazz_id=clazz_id)
        except Student.DoesNotExist:
            messages.error(request, "Sinh viên bạn đang tìm không tồn tại.")
    context = {
        'clazz': clazz,
        'students': students
    }

    return render(request, 'admin_template/class_details.html', context)


def remove_student_from_clazz(request, clazz_id, student_id):
    clazz = get_object_or_404(Clazz, pk=clazz_id)
    student = get_object_or_404(Student, student_id=student_id)

    if request.method == 'POST':
        clazz.students.remove(student)
        return redirect('main_app:admin_class_detail', clazz_id=clazz_id)

    context = {
        'clazz': clazz,
        'student': student
    }
    return render(request, 'admin_template/remove_student_from_class.html', context)

def delete_class(request, clazz_id):
    clazz = get_object_or_404(Clazz, pk=clazz_id)
    class_name = clazz.name

    if request.method == 'POST':
        clazz.delete()
        messages.success(request, f"The class '{class_name}' has been deleted.")
        return redirect('main_app:manage_class') 

    context = {
        'clazz': clazz,
    }

    return render(request, 'admin_template/class_list.html', context)

def change_teacher(request):
    pass