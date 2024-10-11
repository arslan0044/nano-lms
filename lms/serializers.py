from rest_framework import serializers
from .models import Category, Course, Lesson, Content, Enrollment, Progress, Certificate
from user_auth.models import User

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


# Course Serializer
class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'created_at', 'updated_at', 'is_published', 'thumbnail']


# Lesson Serializer
class LessonSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'course', 'created_at', 'updated_at']


# Content Serializer
class ContentSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Content
        fields = ['id', 'title', 'description', 'lesson', 'content_type', 'file_url', 'created_at', 'updated_at']


# Enrollment Serializer
class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at', 'status']


# Progress Serializer
class ProgressSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Progress
        fields = ['id', 'student', 'course', 'lesson', 'completed_at']


# Certificate Serializer
class CertificateSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Certificate
        fields = ['id', 'student', 'certificate_url', 'issued_at']

