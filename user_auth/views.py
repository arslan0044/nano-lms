from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import User, Role
from .serializers import UserSerializer, RoleSerializer

# Role ViewSet
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    