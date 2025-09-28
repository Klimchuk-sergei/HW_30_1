from rest_framework.serializers import ModelSerializer
from .models import Payment, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_number",
            "city",
            "avatar",
            "created_at",
            "is_staff",
            "is_superuser",
            "groups",
        )
        read_only_fields = ("id", "created_at", "is_staff", "is_superuser", "groups")


class UserCreateSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "phone_number", "city", "avatar", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            phone_number=validated_data.get("phone_number"),
            city=validated_data.get("city"),
            avatar=validated_data.get("avatar"),
            password=validated_data.get("password"),
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD

    def validate(self, attrs):
        # подменяем username на email
        attrs["username"] = attrs.get("email")
        if not attrs.get("username"):
            raise serializers.ValidationError({"'email': это поле обязательно"})
        if "email" in attrs:
            del attrs["email"]

        data = super().validate(attrs)
        return data
