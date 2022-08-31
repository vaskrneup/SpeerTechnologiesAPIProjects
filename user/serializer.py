from django.contrib.auth import get_user_model
from rest_framework import serializers
from utils.validators import username_validator


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        help_text="Required.",
        write_only=True,
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "password", "is_active", "is_staff", "is_superuser")
        read_only_fields = ("is_staff", "is_active", "is_superuser",)

    def create(self, validated_data: dict):
        user = self.Meta.model.objects.create(
            username=validated_data.get("username")
        )
        user.set_password(validated_data.get("password"))

        return user
