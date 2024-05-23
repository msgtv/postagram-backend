from django.conf import settings

from rest_framework import serializers

from apps.core.abstract.serializers import AbstractSerializer
from apps.core.user.models import User


class UserSerializer(AbstractSerializer):
    name = serializers.SerializerMethodField()

    @staticmethod
    def get_name(obj):
        return obj.name.title()

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        if not rep.get('avatar'):
            rep['avatar'] = settings.DEFAULT_AVATAR_URL

        request = self.context.get('request')

        if request and settings.DEBUG:
            rep['avatar'] = request.build_absolute_uri(rep['avatar'])
        return rep

    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'name',
                  'first_name',
                  'last_name',
                  'bio',
                  'avatar',
                  'email',
                  'is_active',
                  'created',
                  'updated']
        read_only_fields = [
            'is_active',
        ]
