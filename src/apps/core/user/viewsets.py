from rest_framework.permissions import IsAuthenticated

from apps.core.abstract.viewsets import AbstractViewSet
from apps.core.user.serializers import UserSerializer
from apps.core.user.models import User


class UserViewSet(AbstractViewSet):
    http_method_names = [
        'get',
        'patch',
    ]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)

    def get_object(self):
        obj = User.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)

        return obj

