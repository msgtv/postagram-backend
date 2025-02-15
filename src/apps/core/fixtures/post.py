import pytest

from apps.core.fixtures.user import user
from apps.core.post.models import Post


@pytest.fixture
def post(db, user):
    return Post.objects.create(
        author=user,
        body="This is a test post",
    )
