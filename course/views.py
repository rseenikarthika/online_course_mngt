from django.shortcuts import render
from rest_framework.response import Response

# Create your views here.
# Django shell example
from .models import *
from rest_framework import viewsets, status
from .serializers import InstructorSerializer

# get() usage
instructor = Instructor.objects.get(email='ravikarthika2000@gmail.com')
print(instructor)

# first() usage
first_instructor = Instructor.objects.first()
print(first_instructor)

# last() usage
last_instructor = Instructor.objects.last()
print(last_instructor)

# all() usage
all_instructors = Instructor.objects.all()
for instructor in all_instructors:
    print(instructor)

# filter() usage
filtered_instructors = Instructor.objects.filter(first_name='seeni')
for instructor in filtered_instructors:
    print(instructor)

# exclude() usage
excluded_instructors = Instructor.objects.exclude(last_name='karthila')
for instructor in excluded_instructors:
    print(instructor)




# values() usage
instructor_values = Instructor.objects.values('first_name', 'email')
for instructor in instructor_values:
     print(instructor)

# values_list() usage
instructor_names = Instructor.objects.values_list('first_name', 'last_name')
for first_name, last_name in instructor_names:
     print(first_name, last_name)

# count() usage
total_instructors = Instructor.objects.count()
print(total_instructors)

# order_by() usage
instructors_ordered = Instructor.objects.order_by('first_name')
for instructor in instructors_ordered:
     print(instructor)


# Create a new Instructor
new_instructor = Instructor.objects.create(
    first_name='Kannan',
    last_name='Selvi',
    email='kannan@example.com',
    bio='A seasoned instructor in Python programming.'
)

# Output: Instructor created and saved to the database

alternate_instructor = Instructor(
    first_name='seeni',
    last_name='keerthika',
    email='seenikeerthika@example.com',
    bio='A seasoned instructor in Django programming.'
)
new_instructor.save() # Saving the instance to the database


#update() usage on a single object
instructor = Instructor.objects.get(id=1)
instructor.bio = 'Updated bio for test.'
instructor.save()

# update() usage on multiple records
Instructor.objects.filter(id=1).update(bio='testing.')


courses = Course.objects.select_related('instructor').all()
for course in courses:
    print(course.title, course.instructor.name)

courses = Course.objects.prefetch_related('students').all()
for course in courses:
    print(course.title)
    for student in course.students.all():
        print(student.name)

courses_with_lessons = Course.objects.prefetch_related('lesson_course').all()
for course in courses_with_lessons:
    print(course.title)
    for lesson in course.lesson_course.all():
        print(lesson.title)

# Find courses with 'Python' in the title
courses = Course.objects.filter(title__contains='Python')
# Find courses with 'python' in the title, case-insensitive
courses_contain = Course.objects.filter(title__icontains='python')
# Find courses with no description
course = Course.objects.filter(description__isnull=True)

# Find lessons with titles starting with 'Introduction'
lessons = Lesson.objects.filter(title__startswith='Introduction')

# Find lessons with titles ending with 'Basics'
lesson = Lesson.objects.filter(title__endswith='Basics')



class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instructor = self.get_object()
        serializer = self.get_serializer(instructor)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # Override the partial_update method (PATCH)

    def partial_update(self, request, *args, **kwargs):
        instructor = self.get_object()
        serializer = self.get_serializer(instructor, data=request.data, partial=True)

        # Validate the data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)