import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
class TestSignup:
    def test_user_can_signup(self, api_client):
        """Test that a new user can sign up successfully."""
        data = {'username': 'newuser', 'password': 'newpassword123'}
        url = reverse('signup')
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_proper_data_returned_on_signup(self, api_client):
        """Test that the signup endpoint returns the correct data."""
        data = {'username': 'newuser', 'password': 'newpassword123'}
        url = reverse('signup')
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == 'newuser'
        assert 'token' in response.data
        assert 'password' not in response.data


class TestLogin:
    def test_api_returns_token_for_successful_login(self, api_client, user):
        """Test that the API returns a token for successful login."""
        data = {'username': user.username, 'password': user.raw_password}
        url = reverse('login')
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data

    def test_login_with_invalid_password(self, api_client, user):
        """Test that login fails with an invalid password."""
        data = {'username': user.username, 'password': 'wrongpass'}
        url = reverse('login')
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_token_not_duplicate_if_user_already_logged_in(
        self, api_client, user
    ):
        """Test that logging in again does not create a duplicate token."""
        data = {'username': user.username, 'password': user.raw_password}
        url = reverse('login')
        response1 = api_client.post(url, data)
        response2 = api_client.post(url, data)

        assert response1.data['token'] == response2.data['token']
        assert Token.objects.filter(user=user).count() == 1
