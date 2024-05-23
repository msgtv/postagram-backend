from rest_framework import status

from apps.core.fixtures.user import (
    user,
    data_user
)
from apps.core.fixtures.post import post


class TestUserViewSet:
    endpoint = '/api/user/'

    second_user_data = {
        'username': 'test_user1',
        'email': 'test_email2@mail.ru',
        'first_name': 'test_first',
        'last_name': 'test_last',
        'password': 'test_user213123'
    }

    def test_list(self, client, user):
        client.force_authenticate(user)

        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_retrieve(self, client, user):
        client.force_authenticate(user)

        response = client.get(self.endpoint
                              + str(user.public_id)
                              + '/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username

    def test_create(self, client, user):
        client.force_authenticate(user)

        response = client.post(self.endpoint,
                               self.second_user_data)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_update(self, client, user):
        client.force_authenticate(user)

        data = {'first_name': 'updated_first_name'}

        response = client.patch(self.endpoint
                                + str(user.public_id)
                                + '/',
                                data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'updated_first_name'

    def test_list_anonymous(self, client, user):
        response = client.get(self.endpoint)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_anonymous(self, client, user):
        response = client.get(self.endpoint
                              + str(user.public_id)
                              + '/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_anonymous(self, client, user):
        response = client.post(self.endpoint,
                               self.second_user_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_anonymous(self, client, user):
        data = {'first_name': 'updated_first_name'}

        response = client.patch(self.endpoint
                                  + str(user.public_id)
                                  + '/',
                                  data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
