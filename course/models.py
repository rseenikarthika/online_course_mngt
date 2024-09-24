
from django.db import models

class Instructor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    enrollment_date = models.DateField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in hours")
    start_date = models.DateField()
    end_date = models.DateField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='course_instructor')
    students = models.ManyToManyField(Student, related_name='course_enrollment')

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson_course')

    def __str__(self):
        return self.title


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assignments_lesson')

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='enrollment_student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='enrollment_course')
    enrollment_date = models.DateField()
    completion_status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student} enrolled in {self.course}'


class Progress(models.Model):
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='progress_student')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_lesson')

    def __str__(self):
        return f'{self.student} progress in {self.lesson}: {self.progress_percentage}%'