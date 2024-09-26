from fuzzywuzzy import fuzz
from rest_framework import serializers
from .models import Instructor, Student, Course, Lesson, Assignment, Enrollment, Progress
from datetime import date
from nltk.tokenize import word_tokenize


class InstructorSerializer(serializers.ModelSerializer):
    name_fuzz = serializers.SerializerMethodField()
    # name_tokenize = serializers.SerializerMethodField()
    class Meta:
        model = Instructor
        fields = ['first_name', 'last_name', 'email', 'bio','name_fuzz']

    def to_internal_value(self, data):
        return super().to_internal_value(data)

    # Custom validation for email
    def validate_email(self, value):
        if not value.endswith('@example.com'):
            raise serializers.ValidationError("Email must be an '@example.com' email.")
        return value

    def get_name_fuzz(self,obj):
        # fuzz.ratio(obj.first_name, obj.last_name)
        # fuzz.partial_ratio(obj.first_name, obj.last_name)
       return fuzz.token_sort_ratio(obj.first_name,obj.last_name)

    # def get_name_tokenize(self, obj):
    #     return word_tokenize(obj.first_name)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'enrollment_date']

    # Custom validation for enrollment date
    def validate_enrollment_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Enrollment date cannot be in the future.")
        return value

    def to_representation(self, instance):
        return {
            'first_name':instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'enrollment_date': instance.enrollment_date,
        }

    def to_internal_value(self, data):
        return super().to_internal_value(data)


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

    def to_internal_value(self, data):
        return super().to_internal_value(data)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'course']

    def to_internal_value(self, data):
        return super().to_internal_value(data)

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
