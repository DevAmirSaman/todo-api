import io
import shutil
import tempfile

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
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


@pytest.fixture
def image():
    file = io.BytesIO()
    Image.new('RGB', (100, 100), color='red').save(file, format='PNG')
    file.seek(0)

    return SimpleUploadedFile(
        name='avatar.png', content=file.read(), content_type='image/png'
    )


@pytest.fixture(autouse=True)
def media_temp(settings):
    temp_dir = tempfile.mkdtemp()
    settings.MEDIA_ROOT = temp_dir
    yield
    shutil.rmtree(temp_dir)
