from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Student, Book, Reservation
from django.db.models import Avg, Count, Q, Case, When, Value, CharField
import json

@login_required
def dashboard(request):
    total_students = Student.objects.count()
    avg_gpa = Student.objects.aggregate(Avg('gpa'))['gpa__avg']

    # Student year distribution for pie chart
    years_dict = {}
    for student in Student.objects.all():
        if student.year in years_dict:
            years_dict[student.year] += 1
        else:
            years_dict[student.year] = 1
    year_labels = list(years_dict.keys())
    year_counts = list(years_dict.values())
    
    # GPA distribution with meaningful ranges
    gpa_ranges = {
        '3.81-4.0': Student.objects.filter(gpa__gte=3.81).count(),
        '3.61-3.80': Student.objects.filter(gpa__gte=3.61, gpa__lt=3.80).count(),
        '3.41-3.60': Student.objects.filter(gpa__gte=3.41, gpa__lt=3.60).count(),
        '3.21-3.40': Student.objects.filter(gpa__gte=3.21, gpa__lt=3.40).count(),
        'Below 3.2': Student.objects.filter(gpa__lt=3.2).count()
    }
    
    gpa_labels = list(gpa_ranges.keys())
    gpa_counts = list(gpa_ranges.values())
    
    context = {
        'total_students': total_students,
        'avg_gpa': round(avg_gpa, 2) if avg_gpa else 0,
        'year_labels': year_labels,
        'year_counts': year_counts,
        'gpa_labels': gpa_labels,
        'gpa_counts': gpa_counts
    }
    print(year_counts, year_labels)
    return render(request, 'library/dashboard.html', context)

@login_required
def student_list(request):
    students = Student.objects.all()
    paginator = Paginator(students, 10)
    page = request.GET.get('page')
    students = paginator.get_page(page)
    return render(request, 'library/student_list.html', {'students': students})

@login_required
def book_list(request):
    books = Book.objects.all().order_by('-times_checked_out')
    paginator = Paginator(books, 10)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    return render(request, 'library/book_list.html', {'books': books})

@login_required
def reserve_book(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        book_id = request.POST.get('book')
        
        try:
            student = Student.objects.get(pk=student_id)
            book = Book.objects.get(pk=book_id)
            
            # Check if student has less than 4 books
            current_reservations = Reservation.objects.filter(student=student).count()
            if current_reservations >= 4:
                messages.error(
                    request,
                    f'Could not place the reservation. {student.first_name} {student.last_name} already has {current_reservations} books reserved which is the maximum'
                    )
                return redirect('reserve_book')
            
            # Check if book is available
            if book.currently_checked_out:
                messages.error(request, f'Could not make the reservation. {book.title} is already reserved')
                return redirect('reserve_book')
            
            # Create reservation
            reservation = Reservation.objects.create(student=student, book=book)
            book.currently_checked_out = True
            book.times_checked_out += 1
            book.save()
            
            messages.success(
                request,
                f'Success! {book.title} has been reserved for {student.first_name} {student.last_name}.'
                f' {student.first_name} {student.last_name} now has {current_reservations + 1} book(s) reserved'
            )
            return redirect('book_list')
            
        except (Student.DoesNotExist, Book.DoesNotExist):
            messages.error(request, 'Invalid selection')
            return redirect('reserve_book')
    
    available_books = Book.objects.filter(currently_checked_out=False)
    students = Student.objects.all()
    return render(request, 'library/reserve_book.html', {
        'books': available_books,
        'students': students
    })