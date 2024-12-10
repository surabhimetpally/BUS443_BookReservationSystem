from django.contrib import admin
from .models import Student, Book, Reservation

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ()  # Empty tuple means no read-only fields
    fields = ['studentid', 'first_name', 'last_name', 'major', 'year', 'gpa']  # Include studentid in fields

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    readonly_fields = ()
    fields = ['bookid', 'title', 'author', 'currently_checked_out', 'times_checked_out']  # Include bookid in fields

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['student', 'book', 'reservation_date']