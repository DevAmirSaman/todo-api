import pytest
import io
from PIL import Image
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class TestUserAPI:
    @pytest.mark.parametrize('method,url_name', [
        ('get', 'user-profile'),
        ('patch', 'user-profile'),
        ('delete', 'user-profile'),
    ])
    def test_user_endpoints_require_authentication(self, api_client, method, url_name):
        """Test that user-profile endpoint require authentication."""
        url = reverse(url_name)

        response = getattr(api_client, method)(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_put_not_allowed_on_user_profile(self, api_client, user):
        """Test that PUT method is not allowed on user profile endpoint."""
        api_client.force_authenticate(user=user)
        url = reverse('user-profile')

        response = api_client.put(url, data={'username': 'newusername'})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_profile_returns_correct_data(self, api_client, user):
        """Test that the user profile endpoint returns correct data."""
        api_client.force_authenticate(user=user)
        url = reverse('user-profile')

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username
        assert response.data['email'] == user.email
        assert response.data['first_name'] == user.first_name
        assert response.data['last_name'] == user.last_name
        assert 'avatar' in response.data

    def test_user_can_update_all_fields_except_avatar(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('user-profile')
        data = {
            'username': 'newusername',
            'email': 'newemail@gmail.com',
            'first_name': 'newfirstname',
            'last_name': 'newlastname',
        }

        response = api_client.patch(url, data)

        assert response.status_code == 200

        user.refresh_from_db()
        for field, value in data.items():
            assert getattr(user, field) == value

    def test_avatar_cannot_be_updated_via_user_endpoint(self, api_client, user, image):
        api_client.force_authenticate(user=user)
        url = reverse('user-profile')

        original_avatar_name = user.avatar.name if user.avatar else None

        response = api_client.patch(url, {'avatar': image}, format='multipart')

        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        updated_avatar_name = user.avatar.name if user.avatar else None

        assert updated_avatar_name == original_avatar_name

    def test_delete_user_removes_user_from_database(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('user-profile')

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(id=user.id).exists()

    def test_delete_user_invalidates_token(self, api_client, user):
        token = Token.objects.create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        url = reverse('user-profile')

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAvatarAPI:
    @pytest.mark.parametrize('method,url_name', [
        ('patch', 'user-avatar'),
        ('delete', 'user-avatar'),
    ])
    def test_user_avatar_endpoints_require_authentication(self, api_client, method, url_name):
        """Test that user-avatar endpoint require authentication."""
        url = reverse(url_name)

        response = getattr(api_client, method)(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_can_upload_avatar(self, api_client, user, image):
        """Test that user can update profile avatar."""
        api_client.force_authenticate(user=user)
        url = reverse('user-avatar')

        response = api_client.patch(url, {'avatar': image}, format='multipart')
        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert user.avatar is not None
        assert user.avatar.name.endswith('avatar.png')

    def test_user_can_delete_avatar(self, api_client, user):
        """Test that user can delete profile avatar."""
        api_client.force_authenticate(user=user)
        url = reverse('user-avatar')

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
