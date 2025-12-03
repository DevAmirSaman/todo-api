import pytest
from django.contrib.auth import get_user_model

from auth_app.serializers import SignupSerializer

User = get_user_model()


@pytest.mark.django_db
class TestSignupSerializer:
    def test_password_too_short(self):
        data = {'username': 'testusername', 'password': '1234567'}
        serializer = SignupSerializer(data=data)

        assert not serializer.is_valid()
        assert 'password' in serializer.errors

    def test_cannot_sign_up_with_existing_username(self, user):
        data = {'username': user.username, 'password': 'anotherpassword123'}
        serializer = SignupSerializer(data=data)

        assert not serializer.is_valid()
        assert 'username' in serializer.errors
