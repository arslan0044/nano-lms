from rest_framework import serializers
from .models import User, Role


# Role Serializer
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "title", "description"]


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all()
    )  # ForeignKey field

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "cnic_number",
            "email",
            "date_joined",
            "is_active",
            "last_login",
            "role",
        ]
        extra_kwargs = {"password": {"write_only": True}, "username": {"read_only": True}}

    def create(self, validated_data):
        # No need to handle role separately as PrimaryKeyRelatedField does it
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        role = validated_data.pop("role", None)

        # Update role if provided
        if role is not None:
            instance.role = role

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
