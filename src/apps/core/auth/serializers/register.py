from rest_framework import serializers

from apps.core.user.serializers import UserSerializer
from apps.core.user.models import User


class RegisterSerializer(UserSerializer):
    """
    Сериализатор для регистрации пользователя
    """

    password = serializers.CharField(max_length=128,
                                     min_length=8,
                                     write_only=True,
                                     required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'bio',
            'avatar',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
