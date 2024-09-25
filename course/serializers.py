from rest_framework import serializers
from .models import Instructor, Student, Course, Lesson, Assignment, Enrollment, Progress
from datetime import date


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['first_name', 'last_name', 'email', 'bio']

    # Custom validation for email
    def validate_email(self, value):
        if not value.endswith('@example.com'):
            raise serializers.ValidationError("Email must be an '@example.com' email.")
        return value


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'enrollment_date']

    # Custom validation for enrollment date
    def validate_enrollment_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Enrollment date cannot be in the future.")
        return value


class CourseSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['title', 'description', 'duration', 'start_date', 'end_date', 'instructor', 'students']

    # Validation to ensure end date is after start date
    def validate(self, data):
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError("End date cannot be before start date.")
        return data


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'course']


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'lesson']

    # Custom validation for due date
    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'enrollment_date', 'completion_status']

    # Custom validation for enrollment date
    def validate_enrollment_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Enrollment date cannot be in the future.")
        return value


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['progress_percentage', 'student', 'lesson']

    # Custom validation for progress percentage
    def validate_progress_percentage(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Progress percentage must be between 0 and 100.")
        return value
