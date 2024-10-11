from django.db import models
from django.utils import timezone
from user_auth.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    


# Course Model
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='courses', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    thumbnail = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title


# Lesson Model
class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Content Model
class Content(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('Video', 'Video'),
        ('PDF', 'PDF'),
        ('Audio', 'Audio'),
        ('Article', 'Article')
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    lesson = models.ForeignKey(Lesson, related_name='contents', on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    file_url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Enrollment Model
class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('Enrolled', 'Enrolled'),
        ('Completed', 'Completed'),
        ('Dropped', 'Dropped')
    ]

    student = models.ForeignKey(User, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Enrolled')

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"


# Progress Model
class Progress(models.Model):
    student = models.ForeignKey(User, related_name='progress', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='progress', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='progress', on_delete=models.CASCADE)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} completed {self.lesson} in {self.course}"


# Certificate Model
class Certificate(models.Model):
    student = models.ForeignKey(User, related_name='certificates', on_delete=models.CASCADE)
    certificate_url = models.CharField(max_length=255)
    issued_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Certificate for {self.student}"

    