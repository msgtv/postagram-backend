from rest_framework import status

from apps.core.fixtures.user import user
from apps.core.fixtures.post import post
from apps.core.fixtures.comment import comment


class TestCommentViewSet:
    endpoint = '/api/post/'

    def test_list(self, client, user, post, comment):
        response = client.get(
            self.endpoint
            + str(post.public_id)
            + "/comment/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_retrieve(self, client, user, post, comment):
        client.force_authenticate(user)

        response = client.get(
            self.endpoint
            + str(post.public_id)
            + '/comment/'
            + str(comment.public_id)
            + "/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == comment.public_id.hex
        assert response.data['body'] == comment.body
        assert response.data['author']['id'] == user.public_id.hex

    def test_update(self, client, user, post, comment):
        client.force_authenticate(user)

        data = {
            'body': 'comment updated body',
            'author': user.public_id.hex,
            'post': post.public_id.hex,
        }

        response = client.put(
            self.endpoint
            + str(post.public_id)
            + "/comment/"
            + str(comment.public_id)
            + "/",
            data=data
        )

        assert response.status_code == status.HTTP_200_OK

    def test_list_anonymous(self, client, post, comment):
        response = client.get(self.endpoint
                              + str(post.public_id)
                              + '/comment/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_retrieve_anonymous(self, client, post, comment):
        response = client.get(self.endpoint
                              + str(post.public_id)
                              + '/comment/'
                              + str(comment.public_id)
                              + '/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_anonymous(self, client, post):
        data = {}

        response = client.post(self.endpoint
                               + str(post.public_id)
                               + '/comment/',
                               data=data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_anonymous(self, client, post, comment):
        data = {}

        response = client.put(self.endpoint
                              + str(post.public_id)
                              + '/comment/'
                              + str(comment.public_id)
                              + '/',
                              data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_anonymous(self, client, post, comment):
        response = client.delete(self.endpoint
                                 + str(post.public_id)
                                 + '/comment/'
                                 + str(comment.public_id)
                                 + '/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
