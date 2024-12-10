from django.db import models

class Student(models.Model):
    studentid = models.IntegerField(primary_key=True)  # Custom primary key
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    year = models.CharField(max_length=20)
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    
    def _str_(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['last_name', 'first_name']

class Book(models.Model):
    bookid = models.IntegerField(primary_key=True)  # Custom primary key
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    currently_checked_out = models.BooleanField(default=False)
    times_checked_out = models.IntegerField(default=0)
    
    def _str_(self):
        return self.title
    
    class Meta:
        ordering = ['-times_checked_out']

class Reservation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)