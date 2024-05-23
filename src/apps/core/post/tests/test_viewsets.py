from rest_framework import status

from apps.core.fixtures.user import user
from apps.core.fixtures.post import post


class TestPostViewSet:
    endpoint = '/api/post/'

    def test_list(self, client, user, post):
        client.force_authenticate(user)
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_retrieve(self, client, user, post):
        client.force_authenticate(user=user)
        response = client.get(self.endpoint + str(post.public_id) + "/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == post.public_id.hex
        assert response.data['body'] == post.body
        assert response.data['author']['id'] == post.author.public_id.hex

    def test_create(self, client, user, post):
        client.force_authenticate(user=user)
        data = {
            'body': "Test POST BODY",
            'author': user.public_id.hex,
        }

        response = client.post(self.endpoint, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['body'] == data['body']
        assert response.data['author']['id'] == user.public_id.hex

    def test_update(self, client, user, post):
        client.force_authenticate(user=user)
        data = {
            'body': 'test updated body',
            'author': user.public_id.hex,
        }

        response = client.put(self.endpoint + str(post.public_id) + "/",
                              data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['body'] == data['body']

    def test_delete(self, client, user, post):
        client.force_authenticate(user=user)
        response = client.delete(self.endpoint + str(post.public_id) + "/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_list_anonymous(self, client, post):
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_retrieve_anonymous(self, client, post):
        response = client.get(self.endpoint + str(post.public_id) + "/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == post.public_id.hex
        assert response.data['body'] == post.body
        assert response.data['author']['id'] == post.author.public_id.hex

    def test_create_anonymous(self, client):
        data = {
            "body": "Test POST BODY",
            "author": "test_user"
        }

        response = client.post(self.endpoint, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_anonymous(self, client, post):
        data = {
            "body": "test updated body",
            "author": "test_user"
        }
        response = client.put(
            self.endpoint + str(post.public_id) + "/",
            data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_anonymous(self, client, post):
        response = client.delete(self.endpoint + str(post.public_id) + "/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED