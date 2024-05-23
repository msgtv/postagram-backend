import pytest

from rest_framework import status

from apps.core.fixtures.user import (
    user,
    data_user
)


class TestAuthenticationViewSet:
    endpoint = '/api/auth/'

    def test_login(self, client, user):
        data = {
            'username': user.username,
            'password': "test_password"
        }

        response = client.post(self.endpoint + "login/",
                               data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['access']
        assert response.data['refresh']
        assert response.data['user']['id'] == user.public_id.hex
        assert response.data['user']['username'] == user.username
        assert response.data['user']['email'] == user.email

    @pytest.mark.django_db
    def register_user(self, client):
        response = client.post(self.endpoint + "register/",
                               data_user)

        assert response.status_code == status.HTTP_201_CREATED

    def refresh_token(self, client, user):
        data = {
            "username": user.username,
            "password": "test_password"
        }

        response = client.post(self.endpoint + "login/",
                               data)

        assert response.status_code == status.HTTP_200_OK

        data_refresh = {"refresh": response.data['refresh']}
        response = client.post(self.endpoint + "refresh/",
                               data_refresh)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['access']

