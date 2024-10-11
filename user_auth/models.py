from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import re
from django.core.validators import MinLengthValidator, MaxLengthValidator


# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, cnic_number, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        if not cnic_number:
            raise ValueError("The CNIC field is required")

        email = self.normalize_email(email)

        user = self.model(email=email, cnic_number=cnic_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, cnic_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, cnic_number, password, **extra_fields)


# Role Model
class Role(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


# User Model
class User(AbstractBaseUser):
    username = models.CharField(
        max_length=255, unique=True, blank=True
    )  # auto-generated or based on role
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cnic_number = models.CharField(
        max_length=13,
        unique=True,
        validators=[MinLengthValidator(13), MaxLengthValidator(13)],
    )
    email = models.EmailField(max_length=255, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    # Custom user manager
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["cnic_number"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.role and self.role.title == "Student":
            if not self.username:
                self.username = self.generate_student_username()
        elif self.role and self.role.title == "Staff":
            self.username = self.cnic_number

        super().save(*args, **kwargs)

    def generate_student_username(self):
        prefix = "NT"

        last_username = (
            User.objects.filter(username__startswith=prefix)
            .order_by("-id")
            .values_list("id", flat=True)
            .first()
        )
        if last_username:
            next_number = last_username + 1
        else:
            next_number = 1
        number = f"{next_number:05d}"
        return f"{prefix}{number}"
