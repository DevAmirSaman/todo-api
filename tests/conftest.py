import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    raw_password = 'password'
    u = User.objects.create_user(username='testuser', password='password')
    u.raw_password = raw_password
    return u
