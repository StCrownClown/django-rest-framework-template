from rest_framework import serializers
from .models import Customer
from django.contrib.auth.models import AnonymousUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "username", "first_name", "last_name", "citizen_id", "mobile", "email", "date_joined"]

    def to_representation(self, instance):
        if isinstance(instance, AnonymousUser):
            return {}
        return super(UserSerializer, self).to_representation(instance)


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "username",
            "password",
            "citizen_id",
            "first_name",
            "last_name",
            "mobile",
            "email",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Customer(
            username=validated_data["username"],
            citizen_id=validated_data["citizen_id"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            mobile=validated_data["mobile"],
            email=validated_data["email"],
            is_active=False,
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
