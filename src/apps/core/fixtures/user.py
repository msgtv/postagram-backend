import pytest

from apps.core.user.models import User


data_user = {
    "username": "test",
    "email": "test@gmail.com",
    "first_name": "test",
    "last_name": "test",
    "password": "test_password",
}


@pytest.fixture
def user(db):
    return User.objects.create_user(**data_user)
